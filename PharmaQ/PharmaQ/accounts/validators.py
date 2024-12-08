from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class ImageSizeValidator:
    def __init__(self, size_in_mb):
        self.size_in_mb = size_in_mb

    def __call__(self, value):
        if value.size > self.size_in_mb * 1024 * 1024:
            raise ValidationError(f'The image is too big. It should be less than {self.size_in_mb} MB.')