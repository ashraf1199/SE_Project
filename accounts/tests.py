from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from myapp.forms import StudentUserForm, StudentExtraForm, AdminSignupForm


class StudentSignupViewTestCaseTrue(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('studentsignup_view')

    def test_signup_form_submission(self):
        data = {
            'username': 'dg0107',
            'email': 'deepthipasamgnana@gmail.com',
            'password': 'Deepthi@0107',
            'first_name': 'Deepthi',
            'last_name': 'Gnana',
            'enrollment':'Masters',
            'branch':'CS'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to studentlogin
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'dg0107')
        self.assertEqual(user.email, 'deepthipasamgnana@gmail.com')
        self.assertTrue(user.check_password('Deepthi@0107'))
        self.assertEqual(user.first_name, 'Deepthi')
        self.assertEqual(user.last_name, 'Gnana')
        self.assertEqual(user.enrollment, 'Masters')
        self.assertEqual(user.branch, 'CS')
        self.assertTrue(user.groups.filter(name='STUDENT').exists())

class StudentSignupViewTestCaseFalse(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('studentsignup_view')

    def test_signup_form_submission(self):
        data = {
            'username': 'dg0107',
            'email': 'deepthipasamgnana@gmail.com',
            'password': 'Deepthi@0107',
            'first_name': 'Deepthi',
            'last_name': 'Gnana',
            'enrollment':'Masters',
            'branch':'CS'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to studentlogin
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'dg0107')
        self.assertEqual(user.email, 'deepthipasamgnana@gmail.com')
        self.assertFalse(user.check_password('Deepthi@0108'))
        self.assertEqual(user.first_name, 'Deepthi')
        self.assertEqual(user.last_name, 'Gnana')
        self.assertEqual(user.enrollment, 'Masters')
        self.assertEqual(user.branch, 'CS')
        self.assertTrue(user.groups.filter(name='STUDENT').exists())


class AdminSignupViewTestCaseTrue(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('adminsignup_view')

    def test_signup_form_submission(self):
        data = {
            'username': 'snr3110',
            'firstname': 'Sreeja',
            'lastname': 'Nandyala',
            'password1': 'Sreeja@2001'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to adminlogin
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'snr3110')
        self.assertEqual(user.firstname, 'Sreeja')
        self.assertEqual(user.lastname, 'Nanyala')
        self.assertTrue(user.check_password('Sreeja@2001'))
        self.assertTrue(user.groups.filter(name='ADMIN').exists())

class AdminSignupViewTestCaseFalse(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('adminsignup_view')

    def test_signup_form_submission(self):
        data = {
            'username': 'snr3110',
            'firstname': 'Sreeja',
            'lastname': 'Nandyala',
            'password1': 'Sreeja@2001'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to adminlogin
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'snr3110')
        self.assertEqual(user.firstname, 'Sreeja')
        self.assertEqual(user.lastname, 'Nanyala')
        self.assertFalse(user.check_password('Sreeja@2002'))
        self.assertTrue(user.groups.filter(name='ADMIN').exists())

class AdminLoginViewTestCaseTrue(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('adminlogin_view')

    def test_login_form_submission(self):
        data = {
            'username': 'snr3110',
            'password1': 'Sreeja@2001'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to admin home
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'snr3110')
        self.assertTrue(user.check_password('Sreeja@2001'))

class AdminLoginViewTestCaseFalse(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('adminlogin_view')

    def test_login_form_submission(self):
        data = {
            'username': 'snr3110',
            'password1': 'Sreeja@2001'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to admin home
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'snr3110')
        self.assertFalse(user.check_password('Sreeja@2002'))

class StudentLoginViewTestCaseTrue(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('studentlogin_view')

    def test_login_form_submission(self):
        data = {
            'username': 'dg0107',
            'password': 'Deepthi@0107'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to student home
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'dg0107')
        self.assertTrue(user.check_password('Deepthi@0107'))

class StudentLoginViewTestCaseFalse(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('studentlogin_view')

    def test_login_form_submission(self):
        data = {
            'username': 'dg0107',
            'password': 'Deepthi@0107'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect to student home
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'dg0107')
        self.assertFalse(user.check_password('Deepthi@0108'))
