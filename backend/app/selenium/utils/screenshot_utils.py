import cloudinary
import cloudinary.uploader
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger()


def cloudinary_configured() -> bool:
    return bool(
        settings.CLOUDINARY_CLOUD_NAME
        and settings.CLOUDINARY_API_KEY
        and settings.CLOUDINARY_API_SECRET
    )


def _configure() -> None:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


def upload_screenshot(image_path: str, public_id: str) -> str | None:
    """Upload a screenshot to Cloudinary and return its URL.

    Returns None if Cloudinary is not configured (e.g. local dev) or the upload
    fails — a missing screenshot must never break a test run.
    """
    if not cloudinary_configured():
        logger.info("Cloudinary not configured; skipping screenshot upload")
        return None
    try:
        _configure()
        result = cloudinary.uploader.upload(
            image_path, public_id=public_id, folder="ai-testpilot", overwrite=True
        )
        return result.get("secure_url")
    except Exception as exc:  # noqa: BLE001 - never let screenshots break a run
        logger.warning("Screenshot upload failed: %s", exc)
        return None
