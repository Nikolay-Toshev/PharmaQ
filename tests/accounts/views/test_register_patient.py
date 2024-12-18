from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


UserModel = get_user_model()


class TestPatientRegistrationView(TestCase):
    def setUp(self):
        self.data = {
            'username': 'testpatient',
            'email': 'patient@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }

    def test__patient_registration__expected_is_approved_to_be_true(self):
        response = self.client.post(reverse('patient-registration'), self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        pharmacist = UserModel.objects.get(username='testpatient')

        self.assertTrue(pharmacist.is_approved)



    def test__patient_registration__expected_is_patient_to_be_true(self):
        response = self.client.post(reverse('patient-registration'), self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        pharmacist = UserModel.objects.get(username='testpatient')


        self.assertTrue(pharmacist.is_patient)


    def test__patient_registration__expected_is_pharmacist_to_be_false(self):
        response = self.client.post(reverse('patient-registration'), self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        pharmacist = UserModel.objects.get(username='testpatient')

        self.assertFalse(pharmacist.is_pharmacist)
