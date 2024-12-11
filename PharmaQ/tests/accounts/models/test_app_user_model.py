import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PharmaQ.accounts.models import AppUser


class AppUserModelTestCase(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create(
            username='test',
            email='test@test.com',
            password='test123test',
        )


    def test__valid_str__expected_to_return_username(self):
        self.assertEqual(self.user.username, 'test')



    def test__save_method_delete_old_profile_img_if_exists_on_profile_img_update__expect_old_profile_img_is_deleted(self):
        old_profile_img = SimpleUploadedFile('old_profile_img', b'old_profile_img', content_type='image/jpeg')

        self.user.profile_img = old_profile_img
        self.user.save()

        old_profile_img_path = self.user.profile_img.path
        self.assertTrue(os.path.exists(old_profile_img_path))

        new_profile_img = SimpleUploadedFile('new_profile_img', b'new_profile_img', content_type='image/jpeg')

        self.user.profile_img = new_profile_img
        self.user.save()

        self.assertFalse(os.path.exists(old_profile_img_path))

        new_profile_img_path = self.user.profile_img.path
        self.assertTrue(os.path.exists(new_profile_img_path))

    def tearDown(self):
        if self.user.profile_img and os.path.exists(self.user.profile_img.path):
            os.remove(self.user.profile_img.path)