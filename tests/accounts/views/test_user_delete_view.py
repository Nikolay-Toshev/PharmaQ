from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()

class TestAppUserDeleteView(TestCase):

    def setUp(self):
        self.user_credentials = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test1234test',
        }

        self.user = UserModel.objects.create_user(**self.user_credentials)

    def test__delete_user__user_field_is_active_is_set_to_false__expected_is_active_to_be_false(self):

        self.client.login(
            username=self.user_credentials['username'],
            password=self.user_credentials['password']
        )

        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user.pk}))

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_active)

    def test__delete_user__logs_out_the_user__expected_user_to_be_logged_out(self):
        self.client.login(
            username=self.user_credentials['username'],
            password=self.user_credentials['password']
        )

        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user.pk}))

        self.user.refresh_from_db()

        response_after_delete = self.client.get(reverse('category-create'))  # protected view
        self.assertRedirects(response_after_delete, f'{reverse('login')}?next={reverse('category-create')}')


