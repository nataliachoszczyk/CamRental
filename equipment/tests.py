from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class UserRegistrationTest(TestCase):

    def test_register_user(self):
        # Prepare the data for registration
        data = {
            'username': 'testuser',
            'password1': 'mexshgjygdc',
            'password2': 'mexshgjygdc',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com'
        }

        response = self.client.post(reverse('register'), data)

        user = get_user_model().objects.get(username='testuser')

        self.assertFalse(user.is_active)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Verify your email', mail.outbox[0].subject)

    # def test_invalid_email_verification(self):
    #     invalid_uid = 'invalid_uid'
    #     invalid_token = 'invalid_token'
    #
    #     response = self.client.get(reverse('email_verify', kwargs={'uidb64': invalid_uid, 'token': invalid_token}))
    #
    #     self.assertContains(response, 'Invalid or expired verification link.')
    #     self.assertEqual(response.status_code, 200)

    def test_valid_email_verification(self):

        data = {
            'username': 'testuser',
            'password1': 'mexshgjygdc',
            'password2': 'mexshgjygdc',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com'
        }

        response = self.client.post(reverse('register'), data)
        user = get_user_model().objects.get(username='testuser')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = get_random_string(length=32)
        verification_link = reverse('email_verify', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(verification_link)

        user.refresh_from_db()
        self.assertTrue(user.is_active)

        self.assertRedirects(response, reverse('login'))


# class UserLoginTest(TestCase):
#
#     def test_login_valid_user(self):
#         user = get_user_model().objects.create_user(username='testuser', password='mexshgjygdc')
#
#         response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'mexshgjygdc'})
#
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('home'))


class UserProfileTest(TestCase):

    def test_user_profile_view(self):
        user = get_user_model().objects.create_user(username='testuser', password='mexshgjygdc')
        self.client.login(username='testuser', password='mexshgjygdc')

        response = self.client.get(reverse('user_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_logout_user(self):
        user = get_user_model().objects.create_user(username='testuser', password='mexshgjygdc')
        self.client.login(username='testuser', password='mexshgjygdc')

        response = self.client.post(reverse('user_profile'), {'logout': 'true'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))