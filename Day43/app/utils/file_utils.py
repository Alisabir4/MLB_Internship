from pathlib import Path
import uuid


# --------------------------------------------------
# Directories
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# File Validation Configuration
# --------------------------------------------------

MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
}


# --------------------------------------------------
# Validate Video Filename
# --------------------------------------------------

def validate_video_filename(
    filename: str,
) -> bool:
    """
    Check whether the filename has a supported
    video extension.
    """

    if not filename:
        return False

    extension = Path(
        filename
    ).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


# --------------------------------------------------
# Validate File Size
# --------------------------------------------------

def validate_video_size(
    file_size: int,
) -> bool:
    """
    Check whether the uploaded video is within
    the maximum allowed file size.
    """

    if file_size < 0:
        return False

    return file_size <= MAX_VIDEO_SIZE


# --------------------------------------------------
# Get File Extension
# --------------------------------------------------

def get_file_extension(
    filename: str,
) -> str:
    """
    Return the normalized file extension.
    """

    if not filename:
        return ""

    return Path(
        filename
    ).suffix.lower()


# --------------------------------------------------
# Generate Job ID
# --------------------------------------------------

def generate_job_id() -> str:
    """
    Generate a unique job ID.
    """

    return f"job_{uuid.uuid4().hex[:12]}"


# --------------------------------------------------
# Get Upload Path
# --------------------------------------------------

def get_upload_path(
    job_id: str,
    filename: str,
) -> Path:
    """
    Generate a safe upload path using the job ID
    and original file extension.
    """

    extension = get_file_extension(
        filename
    )

    return (
        UPLOAD_DIR
        / f"{job_id}{extension}"
    )


# --------------------------------------------------
# Get Output Path
# --------------------------------------------------

def get_output_path(
    job_id: str,
) -> Path:
    """
    Generate the processed video output path.
    """

    return (
        OUTPUT_DIR
        / f"{job_id}_processed.mp4"
    )