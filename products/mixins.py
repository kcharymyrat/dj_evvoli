import os

from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ImageValidationMixin:
    MAX_IMAGE_SIZE = 12 * 1024 * 1024  # 12 MB
    MIN_RESOLUTIONS = (200, 200)
    MAX_RESOLUTIONS = (1400, 1000)

    def clean_image(self):
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
                raise ValidationError(
                    f"{min_message} {min_width}x{min_height}" + _("pixels") + "!"
                )

            if img.width > max_width or img.height > max_height:
                max_message = _("Please upload an image with a maximum resolution of")
                raise ValidationError(
                    f"{max_message} {max_width}x{max_height}" + _("pixels") + "!"
                )


class VideoValidationMixin:
    MAX_VIDEO_SIZE = 20 * 1024 * 1024  # 20 MB
    VIDEO_TYPES = (
        "video/mp4",
        "video/quicktime",
        "video/x-matroska",
    )

    def clean_video(self):
        video = getattr(self, "video", None)

        if video:
            file_extension = os.path.splitext(self.video.name)[1][1:].lower()
            print("file_extension =", file_extension)
            file_size = self.video.size
            if file_extension not in ["mp4", "mov", "mkv"]:
                raise ValidationError(
                    _("Unsupported file type. Only mp4, mov, and mkv are supported.")
                )
            if file_size > self.MAX_VIDEO_SIZE:  # 20 MB
                raise ValidationError(
                    _("Make sure that your video is less than 20 MB.")
                )
