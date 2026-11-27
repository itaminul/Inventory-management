import os
import uuid
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Set
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE_TYPES: Set[str] = {"image/jpeg", "image/png", "image/webp"}
DEFAULT_MAX_SIZE_MB = 5


async def upload_single_image(
    file: UploadFile,
    subfolder: str = "general",
    max_size_mb: int = DEFAULT_MAX_SIZE_MB,
    allowed_types: Optional[Set[str]] = None,
) -> dict:
    """
    Validates and saves a single image file to disk.
    Returns a dict containing path, file size (bytes), and dimensions.
    """
    valid_types = allowed_types or ALLOWED_IMAGE_TYPES
    if file.content_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: {', '.join(valid_types)}",
        )

    content = file.file.read()
    file_size = len(content)
    max_bytes = max_size_mb * 1024 * 1024

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if file_size > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File '{file.filename}' exceeds the {max_size_mb}MB limit.",
        )

    # Verify it is a real image and extract width/height
    try:
        with Image.open(BytesIO(content)) as img:
            width, height = img.size
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file.")

    target_dir = UPLOAD_DIR / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    ext = os.path.splitext(file.filename or "")[1].lower() or ".jpg"
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    destination = target_dir / unique_filename

    with open(destination, "wb") as f:
        f.write(content)

    return {
        "url": str(destination).replace("\\", "/"),
        # "size": file_size,        # Size in bytes
        # "width": width,           # Width in pixels
        # "height": height,         # Height in pixels
    }


async def upload_multiple_images(
    files: List[UploadFile],
    subfolder: str = "general",
    max_size_mb: int = DEFAULT_MAX_SIZE_MB,
    max_files: int = 10,
    allowed_types: Optional[Set[str]] = None,
) -> List[dict]:
    """
    Validates and saves multiple image files to disk.
    Rolls back already-saved files if any file in the batch fails validation.
    """
    if not files:
        return []

    if len(files) > max_files:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot upload more than {max_files} images at once.",
        )

    saved_items: List[dict] = []
    try:
        for file in files:
            # Skip empty form file inputs
            if not file.filename:
                continue
            item = await upload_single_image(
                file=file,
                subfolder=subfolder,
                max_size_mb=max_size_mb,
                allowed_types=allowed_types,
            )
            saved_items.append(item)
    except Exception:
        # Clean up any files already written in this batch if an error occurs
        for item in saved_items:
            delete_image_file(item["url"])
        raise

    return saved_items


def delete_image_file(file_url: str) -> None:
    """Safely deletes a file from disk when updating or deleting a record."""
    if not file_url:
        return
    path = Path(file_url)
    if path.exists() and path.is_file():
        path.unlink()
