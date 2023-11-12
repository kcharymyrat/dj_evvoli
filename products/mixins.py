from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ImageValidationMixin:
    MAX_IMAGE_SIZE = 12 * 1024 * 1024  # 12 MB
    MIN_RESOLUTIONS = (200, 200)
    MAX_RESOLUTIONS = (1000, 1000)

    def clean_image(self):
        print("clean_image: self.image =", self.image)

        image = self.image
        min_width, min_height = self.MIN_RESOLUTIONS
        max_width, max_height = self.MAX_RESOLUTIONS

        if image:
            img = Image.open(image)
            min_width, min_height = self.MIN_RESOLUTIONS
            max_width, max_height = self.MAX_RESOLUTIONS

            if image.size > self.MAX_IMAGE_SIZE:
                message = _("Make sure that your image is less than")
                raise ValidationError(
                    f"{message} {self.MAX_IMAGE_SIZE / (1024 * 1024)} MB!"
                )

            if img.width < min_width or img.height < min_height:
                min_message = _("Please upload an image with a minimum resolution of")
                raise ValidationError(f"{min_message} {min_width}x{min_height} pixels!")

            if img.width > max_width or img.height > max_height:
                max_message = _("Please upload an image with a maximum resolution of")
                raise ValidationError(f"{max_message} {max_width}x{max_height} pixels!")


class VideoValidationMixin:
    MAX_VIDEO_SIZE = 20 * 1024 * 1024  # 20 MB
    VIDEO_TYPES = (
        "video/mp4",
        "video/quicktime",
        "video/x-matroska",
    )

    def clean_video(self):
        print("clean_video: self.video =", self.video)
        video = self.video

        if self.video:
            if video.file.content_type not in self.VIDEO_TYPES:
                raise ValidationError(
                    {
                        "video": _(
                            "Unsupported file type. Only mp4, quicktime, and mkv are supported."
                        )
                    }
                )
            if video.size > self.MAX_VIDEO_SIZE:
                message = _("Make sure that your video less than")
                raise ValidationError(
                    {"video": f"{message} {self.MAX_VIDEO_SIZE / (1024 * 1024)} MB!"}
                )
