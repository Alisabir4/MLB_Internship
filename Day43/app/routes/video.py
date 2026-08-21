from pathlib import Path
import logging
import re
import time

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import FileResponse

from app.services.video_processor import process_video

from app.utils.file_utils import (
    ALLOWED_EXTENSIONS,
    MAX_VIDEO_SIZE,
    generate_job_id,
    get_output_path,
    get_upload_path,
    validate_video_filename,
    validate_video_size,
)


router = APIRouter(
    prefix="/video",
    tags=["Video Processing"],
)


# --------------------------------------------------
# Logger
# --------------------------------------------------

logger = logging.getLogger("ai_video_api")


# --------------------------------------------------
# In-memory job storage
# --------------------------------------------------

jobs = {}


# --------------------------------------------------
# Job ID Validation
# --------------------------------------------------

def validate_job_id(job_id: str) -> bool:
    """
    Validate the basic format of a job ID.
    """

    if not job_id:
        return False

    if len(job_id) > 100:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9_-]+",
            job_id,
        )
    )


# --------------------------------------------------
# Background Video Processing
# --------------------------------------------------

def process_video_background(
    job_id: str,
    input_path: str,
    output_path: str,
    confidence: float,
):
    """
    Background task that processes the uploaded video.
    """

    start_time = time.time()

    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 0

        jobs[job_id]["processing_start_time"] = (
            time.strftime("%Y-%m-%d %H:%M:%S")
        )

        logger.info(
            f"Job started | "
            f"job_id={job_id} "
            f"confidence={confidence}"
        )

        def update_progress(progress: int):
            jobs[job_id]["progress"] = progress

        # --------------------------------------------------
        # Process video
        # --------------------------------------------------

        stats = process_video(
            input_path=input_path,
            output_path=output_path,
            progress_callback=update_progress,
            confidence=confidence,
            job_id=job_id,
        )

        # --------------------------------------------------
        # Processing completed
        # --------------------------------------------------

        processing_time = round(
            time.time() - start_time,
            3,
        )

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["statistics"] = stats

        jobs[job_id]["processing_end_time"] = (
            time.strftime("%Y-%m-%d %H:%M:%S")
        )

        jobs[job_id]["processing_time_seconds"] = (
            processing_time
        )

        logger.info(
            f"Processing completed | "
            f"job_id={job_id} "
            f"processing_time={processing_time}s"
        )

    except Exception as e:

        processing_time = round(
            time.time() - start_time,
            3,
        )

        jobs[job_id]["status"] = "failed"
        jobs[job_id]["progress"] = 0

        # Keep internal exception details out
        # of the API response.
        jobs[job_id]["error"] = (
            "Video processing failed."
        )

        jobs[job_id]["processing_end_time"] = (
            time.strftime("%Y-%m-%d %H:%M:%S")
        )

        jobs[job_id]["processing_time_seconds"] = (
            processing_time
        )

        logger.error(
            f"Video processing failed | "
            f"job_id={job_id} "
            f"processing_time={processing_time}s "
            f"error={str(e)}",
            exc_info=True,
        )


# --------------------------------------------------
# Process Video
# --------------------------------------------------

@router.post("/process")
async def process_video_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    confidence: float = Query(
        default=0.40,
        ge=0.0,
        le=1.0,
        description=(
            "YOLO confidence threshold "
            "between 0.0 and 1.0"
        ),
    ),
):
    """
    Upload a video and start background YOLO processing.
    """

    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    # --------------------------------------------------
    # Check file object
    # --------------------------------------------------

    if file is None:
        raise HTTPException(
            status_code=400,
            detail="Video file is required.",
        )

    # --------------------------------------------------
    # Check filename
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    # --------------------------------------------------
    # Validate extension
    # --------------------------------------------------

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:

        logger.warning(
            f"Unsupported file format | "
            f"request_id={request_id} "
            f"extension={file_extension}"
        )

        raise HTTPException(
            status_code=415,
            detail=(
                "Unsupported video format. "
                "Allowed formats: MP4, AVI, MOV, MKV."
            ),
        )

    # Additional filename validation
    if not validate_video_filename(
        file.filename
    ):

        logger.warning(
            f"Video filename validation failed | "
            f"request_id={request_id}"
        )

        raise HTTPException(
            status_code=415,
            detail=(
                "Unsupported video format. "
                "Allowed formats: MP4, AVI, MOV, MKV."
            ),
        )

    # --------------------------------------------------
    # Generate job ID
    # --------------------------------------------------

    job_id = generate_job_id()

    logger.info(
        f"Video upload received | "
        f"request_id={request_id} "
        f"job_id={job_id}"
    )

    # --------------------------------------------------
    # Generate file paths
    # --------------------------------------------------

    upload_path = get_upload_path(
        job_id,
        file.filename,
    )

    output_path = get_output_path(
        job_id,
    )

    try:

        total_size = 0

        # --------------------------------------------------
        # Read file in chunks
        # --------------------------------------------------

        with open(
            upload_path,
            "wb",
        ) as buffer:

            while True:

                chunk = await file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                total_size += len(chunk)

                # --------------------------------------------------
                # File size validation
                # --------------------------------------------------

                if not validate_video_size(
                    total_size
                ):

                    if Path(
                        upload_path
                    ).exists():

                        Path(
                            upload_path
                        ).unlink()

                    logger.warning(
                        f"Video file too large | "
                        f"request_id={request_id} "
                        f"job_id={job_id} "
                        f"size={total_size}"
                    )

                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "Video file is too large. "
                            f"Maximum allowed size is "
                            f"{MAX_VIDEO_SIZE // (1024 * 1024)} MB."
                        ),
                    )

                buffer.write(chunk)

        # --------------------------------------------------
        # Empty file validation
        # --------------------------------------------------

        if total_size == 0:

            if Path(
                upload_path
            ).exists():

                Path(
                    upload_path
                ).unlink()

            logger.warning(
                f"Empty video file | "
                f"request_id={request_id} "
                f"job_id={job_id}"
            )

            raise HTTPException(
                status_code=400,
                detail="Uploaded video is empty.",
            )

    except HTTPException:
        raise

    except Exception as e:

        if Path(
            upload_path
        ).exists():

            try:
                Path(
                    upload_path
                ).unlink()
            except Exception:
                pass

        logger.error(
            f"Failed to save uploaded video | "
            f"request_id={request_id} "
            f"job_id={job_id} "
            f"error={str(e)}",
            exc_info=True,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to save uploaded video.",
        )

    # --------------------------------------------------
    # Create job
    # --------------------------------------------------

    jobs[job_id] = {
        "job_id": job_id,
        "request_id": request_id,
        "status": "queued",
        "progress": 0,
        "statistics": None,
        "error": None,
        "confidence": confidence,
        "file_size_bytes": total_size,
        "processing_start_time": None,
        "processing_end_time": None,
        "processing_time_seconds": None,
    }

    # --------------------------------------------------
    # Start background task
    # --------------------------------------------------

    background_tasks.add_task(
        process_video_background,
        job_id,
        str(upload_path),
        str(output_path),
        confidence,
    )

    logger.info(
        f"Job queued | "
        f"request_id={request_id} "
        f"job_id={job_id} "
        f"file_size={total_size} "
        f"confidence={confidence}"
    )

    return {
        "success": True,
        "request_id": request_id,
        "job_id": job_id,
        "status": "processing",
        "confidence": confidence,
    }


# --------------------------------------------------
# Video Status
# --------------------------------------------------

@router.get("/status/{job_id}")
async def get_video_status(
    job_id: str,
):
    """
    Get processing status and progress for a video job.
    """

    # --------------------------------------------------
    # Validate job ID format
    # --------------------------------------------------

    if not validate_job_id(job_id):

        raise HTTPException(
            status_code=400,
            detail="Invalid job ID format.",
        )

    # --------------------------------------------------
    # Check job ID
    # --------------------------------------------------

    if job_id not in jobs:

        raise HTTPException(
            status_code=404,
            detail="Job ID not found.",
        )

    job = jobs[job_id]

    response = {
        "success": True,
        "request_id": job["request_id"],
        "job_id": job_id,
        "status": job["status"],
        "progress": job["progress"],
    }

    # --------------------------------------------------
    # Add statistics
    # --------------------------------------------------

    if job["statistics"] is not None:

        response["statistics"] = (
            job["statistics"]
        )

    # --------------------------------------------------
    # Add processing timestamps
    # --------------------------------------------------

    if job["processing_start_time"]:

        response["processing_start_time"] = (
            job["processing_start_time"]
        )

    if job["processing_end_time"]:

        response["processing_end_time"] = (
            job["processing_end_time"]
        )

    if job["processing_time_seconds"] is not None:

        response["processing_time_seconds"] = (
            job["processing_time_seconds"]
        )

    # --------------------------------------------------
    # Add error
    # --------------------------------------------------

    if job["error"] is not None:

        response["error"] = job["error"]

    return response


# --------------------------------------------------
# Video Result
# --------------------------------------------------

@router.get("/result/{job_id}")
async def get_video_result(
    job_id: str,
):
    """
    Download the processed video after completion.
    """

    # --------------------------------------------------
    # Validate job ID
    # --------------------------------------------------

    if not validate_job_id(job_id):

        raise HTTPException(
            status_code=400,
            detail="Invalid job ID format.",
        )

    # --------------------------------------------------
    # Check job ID
    # --------------------------------------------------

    if job_id not in jobs:

        raise HTTPException(
            status_code=404,
            detail="Job ID not found.",
        )

    job = jobs[job_id]

    # --------------------------------------------------
    # Still processing
    # --------------------------------------------------

    if job["status"] in [
        "queued",
        "processing",
    ]:

        raise HTTPException(
            status_code=202,
            detail="Video is still being processed.",
        )

    # --------------------------------------------------
    # Processing failed
    # --------------------------------------------------

    if job["status"] == "failed":

        raise HTTPException(
            status_code=500,
            detail=(
                job["error"]
                or "Video processing failed."
            ),
        )

    # --------------------------------------------------
    # Get output path
    # --------------------------------------------------

    output_path = get_output_path(
        job_id,
    )

    # --------------------------------------------------
    # Check output file
    # --------------------------------------------------

    if not Path(
        output_path
    ).exists():

        raise HTTPException(
            status_code=404,
            detail="Processed video not found.",
        )

    logger.info(
        f"Processed video downloaded | "
        f"request_id={job['request_id']} "
        f"job_id={job_id}"
    )

    # --------------------------------------------------
    # Return processed video
    # --------------------------------------------------

    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=(
            f"{job_id}_processed.mp4"
        ),
    )