from unittest import TestCase

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from PharmaQ.accounts.validators import ImageSizeValidator


class TestImageSizeValidator(TestCase):
    def setUp(self):
        self.validator = ImageSizeValidator(5)


    def test__valid_image_size__expect_no_errors(self):
        image = SimpleUploadedFile('image.jpg', b'i' * (4 * 1024 * 1024), content_type='image/jpeg')

        self.validator(image)

    def test__invalid_image_size__expect_errors(self):
        image = SimpleUploadedFile('image.jpg', b'i' * (6 * 1024 * 1024), content_type='image/jpeg')

        with self.assertRaises(ValidationError) as e:
            self.validator(image)

        self.assertEqual(str(e.exception), "['The image is too big. It should be less than 5 MB.']")
