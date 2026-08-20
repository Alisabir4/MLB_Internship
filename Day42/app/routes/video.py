
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services.video_processor import process_video
from app.utils.file_utils import (
    generate_job_id,
    get_output_path,
    get_upload_path,
    validate_video_filename,
)


router = APIRouter(
    prefix="/video",
    tags=["Video Processing"],
)


# In-memory job storage
jobs = {}


def process_video_background(
    job_id: str,
    input_path: str,
    output_path: str,
):
    """
    Background task that processes the uploaded video using YOLO.
    """

    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 0

        def update_progress(progress: int):
            jobs[job_id]["progress"] = progress

        # Process video
        stats = process_video(
            input_path=input_path,
            output_path=output_path,
            progress_callback=update_progress,
        )

        # Processing completed
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["statistics"] = stats

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["progress"] = 0
        jobs[job_id]["error"] = str(e)


@router.post("/process")
async def process_video_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Upload a video and start background YOLO processing.
    """

    # Check file object
    if file is None:
        raise HTTPException(
            status_code=400,
            detail="Video file is required.",
        )

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    # Validate extension
    if not validate_video_filename(file.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported video format. "
                "Allowed formats: MP4, AVI, MOV, MKV."
            ),
        )

    # Generate unique job ID
    job_id = generate_job_id()

    # Generate file paths
    upload_path = get_upload_path(
        job_id,
        file.filename,
    )

    output_path = get_output_path(job_id)

    try:
        # Read uploaded file
        content = await file.read()

        # Check empty file
        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded video is empty.",
            )

        # Save uploaded video
        with open(upload_path, "wb") as buffer:
            buffer.write(content)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded video: {str(e)}",
        )

    # Create job information
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "statistics": None,
        "error": None,
    }

    # Start background processing
    background_tasks.add_task(
        process_video_background,
        job_id,
        str(upload_path),
        str(output_path),
    )

    return {
        "job_id": job_id,
        "status": "processing",
    }


@router.get("/status/{job_id}")
async def get_video_status(job_id: str):
    """
    Get processing status and progress for a video job.
    """

    # Check job ID
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job ID not found.",
        )

    job = jobs[job_id]

    response = {
        "job_id": job_id,
        "status": job["status"],
        "progress": job["progress"],
    }

    # Add statistics when processing is complete
    if job["statistics"] is not None:
        response["statistics"] = job["statistics"]

    # Add error when processing fails
    if job["error"] is not None:
        response["error"] = job["error"]

    return response


@router.get("/result/{job_id}")
async def get_video_result(job_id: str):
    """
    Download the processed video after completion.
    """

    # Check job ID
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job ID not found.",
        )

    job = jobs[job_id]

    # Still processing
    if job["status"] in ["queued", "processing"]:
        raise HTTPException(
            status_code=202,
            detail="Video is still being processed.",
        )

    # Processing failed
    if job["status"] == "failed":
        raise HTTPException(
            status_code=500,
            detail=job["error"] or "Video processing failed.",
        )

    # Get output path
    output_path = get_output_path(job_id)

    # Check output file
    if not Path(output_path).exists():
        raise HTTPException(
            status_code=404,
            detail="Processed video not found.",
        )

    # Return processed video
    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"{job_id}_processed.mp4",
    )