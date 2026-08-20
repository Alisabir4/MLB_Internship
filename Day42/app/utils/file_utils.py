from pathlib import Path
import uuid


UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
}


def validate_video_filename(filename: str) -> bool:
    if not filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


def generate_job_id() -> str:
    return uuid.uuid4().hex[:12]


def get_upload_path(job_id: str, filename: str) -> Path:
    extension = Path(filename).suffix.lower()

    return UPLOAD_DIR / f"{job_id}{extension}"


def get_output_path(job_id: str) -> Path:
    return OUTPUT_DIR / f"{job_id}_processed.mp4"