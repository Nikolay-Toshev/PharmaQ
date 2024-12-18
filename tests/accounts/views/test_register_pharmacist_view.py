from select import select

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


UserModel = get_user_model()


class TestPharmacistRegistrationView(TestCase):
    def setUp(self):
        self.professional_card = SimpleUploadedFile('card.jpg', b'test_content', content_type='image/jpeg')
        self.data = {
            'username': 'testpharmacist',
            'email': 'pharmacist@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'professional-card': self.professional_card,
        }

    def test__pharmacist_registration__expected_is_approved_to_be_false(self):

        response = self.client.post(reverse('pharmacist-registration'), self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        pharmacist = UserModel.objects.get(username='testpharmacist')

        self.assertFalse(pharmacist.is_approved)


    def test__pharmacist_registration__expected_is_patient_to_be_false(self):
        response = self.client.post(reverse('pharmacist-registration'), self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        pharmacist = UserModel.objects.get(username='testpharmacist')

        self.assertFalse(pharmacist.is_patient)


    def test__pharmacist_registration__expected_is_pharmacist_to_be_true(self):
        response = self.client.post(reverse('pharmacist-registration'), self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        pharmacist = UserModel.objects.get(username='testpharmacist')

        self.assertTrue(pharmacist.is_pharmacist)

