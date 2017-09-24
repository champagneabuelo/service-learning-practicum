import datetime
import time
from django.utils import timezone
from django.test import TestCase
from georgias.models import VolunteerHours, UserProfile, Donors, Incident_Report
from georgias.forms import *
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import Client
#from datetime import datetime

class VolunteerMethodTests(TestCase):

	def test_submitted_recently(self):
		recent_sub = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=20))
		self.assertEqual(recent_sub.was_submitted_recently(), True)
		#print("submitted in last 30 days")
	def test_submitted_positive_hours_within_daily_limit(self):
		user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user2 = User.objects.create_user('john2', 'lennon2@thebeatles.com', 'john2password')
		call_command("loaddata", "ssb9qu_fix",verbosity=0)	
		allHours = VolunteerHours.objects.all().filter(numHours__gte=0).filter(numHours__lt=24)
		self.assertEqual(allHours.exists(), True)
	def test_submitted_negative_hours(self):
		user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user2 = User.objects.create_user('john2', 'lennon2@thebeatles.com', 'john2password')
		call_command("loaddata", "ssb9qu_fix",verbosity=0)
		allHours = VolunteerHours.objects.all().filter(numHours__lt=0)
		self.assertEqual(allHours.exists(), True)
		#print("submitted negative hours")
	def test_submitted_old(self):
		recent_sub = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40))
		self.assertEqual(recent_sub.was_submitted_recently(), False)	
		#print("submitted past 30 days ago") 
	def test_submitted_zero_hours(self):
		user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
                user2 = User.objects.create_user('john2', 'lennon2@thebeatles.com', 'john2password')
                call_command("loaddata", "avh5nm_fix",verbosity=0)
                allHours = VolunteerHours.objects.all().filter(numHours=0)
                self.assertEqual(allHours.exists(), True)


class VolunteerViewTests(TestCase):
	def setUp(self):
                self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
                self.client.login(username="john", password="johnpassword")
		self.user = User.objects.create_user('john2', 'lennon@thebeatles.com', 'johnpassword2')

	def test_no_hours(self):
		response = self.client.get('/volunteerHours/')
		self.assertQuerysetEqual(response.context['volHours'], [])
	def test_many_hours(self):
		recent_sub = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40), numHours=3, volunteer_id=1)
		recent_sub2 = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40), numHours=2, volunteer_id=1)
		recent_sub.save()
		recent_sub2.save()
		response = self.client.get('/volunteerHours/')
		self.assertEqual(len(response.context['volHours']), 2)


        def test_delete_hours(self):
                recent_sub = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40), numHours=3, volunteer_id=1)
                recent_sub2 = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40), numHours=2, volunteer_id=1)
                recent_sub.save()
                recent_sub2.save()
                self.client.get('/delete_hour/' + str(recent_sub.id))
                response = self.client.get('/volunteerHours/')
                self.assertEqual(len(response.context['volHours']), 1)

	def test_delete_with_no_hours(self):
		resp = self.client.get('/delete_hour/1')
		response = self.client.get('/volunteerHours/')
		self.assertEqual(len(response.context['volHours']), 0)
	
	def test_only_shows_current_user_hours(self):
		recent_sub = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40), numHours=3, volunteer_id=1)
                recent_sub2 = VolunteerHours(volDate = timezone.now() - datetime.timedelta(days=40), numHours=2, volunteer_id=2)
                recent_sub.save()
                recent_sub2.save()
		response = self.client.get('/volunteerHours/')
		self.assertEqual(len(response.context['volHours']), 1)


class UserTestCase(TestCase):
        def setUp(self):
                User.objects.create(username="user1", first_name = "Jack", last_name = "Frost", email = "jfrost@gmail.com", password="pass")
		User.objects.create(username="user2", password="pass")		
		User.objects.create(username="user3", password="pass")
		self.user = User.objects.create_superuser(username='john', first_name='john', last_name='jhn', email='lennon@thebeatles.com', password='johnpassword')
	#	UserProfile.objects.create(user = User.objects.get(username="user1"), user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')


	def test_num_users(self):
		users = User.objects.all().count()
		self.assertEqual(users, 4)

	def test_change_user_to_superuser(self):
		user1 = User.objects.get(username="user1")
		user1.is_superuser = True
		self.assertTrue(user1.is_superuser)

        def test_user_is_active(self):
                user1 = User.objects.get(username="user1")
                self.assertTrue(user1.is_active)
	def test_user_is_disabled(self):
		user1 = User.objects.get(username="user2")
		user1.is_active = False
		self.assertFalse(user1.is_active)
                
        def test_user_is_superuser(self):
                user1 = User.objects.get(username="user1")
                self.assertFalse(user1.is_superuser)
                
	def test_user_is_not_admin(self):
                user1 = User.objects.get(username="user1")
                profile = UserProfile.objects.create(user = user1, user_type = 'STF', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
		self.assertEqual(UserProfile.objects.get(user=user1).user_type, 'STF')
                
        def test_user_is_staff(self):
                user1 = User.objects.get(username="user1")
                self.assertFalse(user1.is_staff)

        def test_user_not_logged_in(self):
                response = self.client.post('/login/', {'username':'user1', 'password':'pass'})
                self.assertEqual(200, response.status_code)

        def test_user_creation(self):
                user1 = User.objects.get(username="user1")
                profile = UserProfile.objects.create(user = user1, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
                self.assertTrue(isinstance(user1, User))
                
        def test_user_profile_creation(self):
                user1 = User.objects.get(username="user1")
                profile = UserProfile.objects.create(user = user1, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
                self.assertTrue(isinstance(profile, UserProfile))

        def test_user_profile_unicode(self):
                user1 = User.objects.get(username="user1")
                profile = UserProfile.objects.create(user = user1, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
                self.assertEqual(profile.__unicode__(), profile.user.username)

        def test_user_staffprofile_view(self):        
		self.client.login(username="john", password="johnpassword")
                profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
		response = self.client.get('/staff_profile/')
		self.assertContains(response, 'john')

	def test_user_adminprofile_view(self):        
		self.client.login(username="john", password="johnpassword")
                profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
		response = self.client.get('/admin_profile/')
		self.assertContains(response, 'john')

	def test_add_staff(self):        
		self.client.login(username="john", password="johnpassword")
                profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
		response = self.client.post('/admin_add_staff/', {'first_name' : 'first', 'last_name':'last', 'username':'firstlast', 'email':'a@a.com', 'password':'firstpass', 'user_type':'ADM'})
		self.assertContains(response, 'successfully')

	def test_add_staff_fail(self):        
		self.client.login(username="john", password="johnpassword")
                profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
		response = self.client.post('/admin_add_staff/')
		self.assertContains(response, 'unable')

	def test_staff_home(self):        
		self.client.login(username="john", password="johnpassword")
                profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
		response = self.client.post('/admin_add_staff/')
		self.assertContains(response, 'unable')


	def test_enable_user(self):        
		self.client.login(username="john", password="johnpassword")
		user5 = User.objects.create(username="user5", password="pass")		
	        profile = UserProfile.objects.create(user = user5, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')	
		user5.is_active=False
		user5.save()
		response = self.client.get('/enable_user/' + str(profile.pk))
		self.assertFalse(profile.user.is_active)

	def test_enable_user_noexist(self):        
		self.client.login(username="john", password="johnpassword")
		#user5 = User.objects.create(username="user5", password="pass")		
	        #profile = UserProfile.objects.create(user = user5, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')	
		#user5.is_active=False
		#user5.save()
		response = self.client.get('/enable_user/6')
		self.assertEquals(response.status_code,302)

	def test_disable_user_noexist(self):        
		self.client.login(username="john", password="johnpassword")
		#user5 = User.objects.create(username="user5", password="pass")		
	        #profile = UserProfile.objects.create(user = user5, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')	
		response = self.client.get('/disable_user/6')
		self.assertEquals(response.status_code,302)

	def test_delete_user_noexist(self):        
		self.client.login(username="john", password="johnpassword")
		self.user.is_superuser=True
		#user5 = User.objects.create(username="user5", password="pass")		
	        #profile = UserProfile.objects.create(user = user5, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')	
		response = self.client.get('/delete_user/6')
		self.assertEquals(response.status_code,302)

	def test_delete_user_noperm(self):        
		self.client.login(username="john", password="johnpassword")
		self.user.is_superuser = False
		#user5 = User.objects.create(username="user5", password="pass")		
	        #profile = UserProfile.objects.create(user = user5, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')	
		response = self.client.get('/delete_user/6')
		self.assertEquals(response.status_code,302)


	def test_disable_user(self):        
		self.client.login(username="john", password="johnpassword")
		user6 = User.objects.create(username="user6", password="pass")		
	        profile = UserProfile.objects.create(user = user6, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')		
		response = self.client.get('/disable_user/' + str(profile.pk))
		self.assertTrue(profile.user.is_active)

	def test_delete_user(self):        
		self.client.login(username="john", password="johnpassword")
		user7 = User.objects.create(username="user7", password="pass")		
	        profile = UserProfile.objects.create(user = user7, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')		
		response = self.client.get('/delete_user/' + str(profile.pk))
		self.assertEquals(len(UserProfile.objects.all()), 0)


	def test_edit_user_profile(self):
		self.client.login(username="john", password="johnpassword")
                UserProfile.objects.create(user = self.user, user_addr = '123 fake st', user_homeph = '888', user_workph = '777')
		response = self.client.post('/user_edit_profile/', {'user_homeph':'999'}, follow=True)
		self.assertContains(response, '999')

	def test_get_edit_user_profile(self):
		self.client.login(username="john", password="johnpassword")
                UserProfile.objects.create(user = self.user, user_addr = '123 fake st', user_homeph = '888', user_workph = '777')
		response = self.client.get('/user_edit_profile/')
		self.assertContains(response, '888')


        def test_user_form_valid_all_data(self):
                user1 = User.objects.get(username="user1")

                data = {'first_name': user1.first_name,
                        'last_name': user1.last_name,
                        'username': user1.username,
                        'email': user1.email,
                        'password': user1.password}
                form = UserForm(data=data)
                self.assertFalse(form.is_valid())

        def test_user_form_invalid(self):
                 user1 = User.objects.get(username="user1")
                 data = {
                         'username': user1.username,
                         'email': user1.email,
                         'password': user1.password,
                         }
                 form = UserForm(data)
                 self.assertFalse(form.is_valid())

        def test_profile_form_valid(self):
                user1 = User.objects.get(username="user1")
                profile = UserProfile.objects.create(user = user1, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
                data = {'user_type' : profile.user_type}

                form = UserProfileForm(data=data)
                self.assertTrue(form.is_valid())

class DonorTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		self.client.login(username="john", password="johnpassword")

	def test_contact(self):
		self.client = Client()
		response = self.client.post('/contact_mail/', {'name':'test', 'from':'test', 'subject':'test', 'message':'test'})
		self.assertContains(response, 'Thank you')

	def test_invalid_donor_email(self):
		self.client = Client()
		response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': 'Smith', 'donorEmail' : 'test', 'donationAmount' : '50'})
		self.assertEqual(response.context['message'], 'Please enter a valid email!')
		self.assertEqual(response.context['error'], True)

	def test_invalid_donor_email_2(self):
		self.client = Client()
		response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': 'Smith', 'donorEmail' : 'test@.com', 'donationAmount' : '50'})
		self.assertEqual(response.context['message'], 'Please enter a valid email!')
		self.assertEqual(response.context['error'], True)

	def test_non_integer_donation_amount(self):
		self.client = Client()
		response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': 'Smith' , 'donorEmail' : 'test@gmail.com', 'donationAmount' : 'one hundred'})
		self.assertEqual(response.context['message'], 'Please enter donation amount as a whole number')
		self.assertEqual(response.context['error'], True)

	def test_invalid_float_donation_amount(self):
                self.client = Client()
                response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': 'Smith', 'donorEmail' : 'test@gmail.com', 'donationAmount' : '50.00'})
                self.assertEqual(response.context['message'], 'Please enter donation amount as a whole number')
		self.assertEqual(response.context['error'], True)

	def test_valid_donor_email(self):
                self.client = Client()
                response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': 'Smith', 'donorEmail' : 'test@gmail.com', 'donationAmount' : '50'})
                self.assertEqual(response.status_code, 302)

	def test_empty_name_input(self):
		self.client = Client()
		response = self.client.post('/donate_online/', {'donorFirstName' : '', 'donorLastName': 'Smith', 'donorEmail' : 'test@gmail.com', 'donationAmount' : '50'})
		self.assertEqual(response.context['message'], 'Make sure all fields are entered and valid.')
		self.assertEqual(response.context['error'], True)

	def test_invalid_first_name_input(self):
                self.client = Client()
                response = self.client.post('/donate_online/', {'donorFirstName' : '32', 'donorLastName': 'Smith', 'donorEmail' : 'test@gmail.com', 'donationAmount' : '50'})
                self.assertEqual(response.context['message'], 'Please enter a valid name.')
                self.assertEqual(response.context['error'], True)

	def test_invalid_last_name_input(self):
                self.client = Client()
                response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': '32', 'donorEmail' : 'test@gmail.com', 'donationAmount' : '50'})
                self.assertEqual(response.context['message'], 'Please enter a valid name.')
                self.assertEqual(response.context['error'], True)                       

	def test_invalid_amount_input(self):
                self.client = Client()
                response = self.client.post('/donate_online/', {'donorFirstName' : 'John', 'donorLastName': 'Smith', 'donorEmail' : 'test@gmail.com', 'donationAmount' : ''})
                self.assertEqual(response.context['message'], 'Make sure all fields are entered and valid.')
                self.assertEqual(response.context['error'], True)

	def test_delete_donation(self):
		donation = Donors.objects.create(id = 1, donorFirstName = "John", donorLastName = "Smith", donationAmount = 10, donationDate = '2016-12-08')
                donation.save()
                self.client.get('/delete_donation/1')
                response = self.client.get('/admin_donate/')
                donors = Donors.objects.all()
                self.assertEqual(len(donors), 0)


        def test_delete_non_existent_donation(self):
                response = self.client.get('/delete_donation/1')
                #response = self.client.get('/admin_donate/')
                self.assertEqual(response.context['error_message'], 'Failed to delete donation.')


	def test_invalid_first_name_edit(self):
                donation = Donors.objects.create(id = 1, donorFirstName = "John", donorLastName = "Smith",  donationAmount = 10, donationDate = '2016-12-08')
                response = self.client.post('/edit_donation/1', {'donorFirstName' : "", 'donorLastName' : "Smith", 'donorEmail' : 'testing@gmail.com', 'donationAmount' : '10'})
                self.assertEqual(response.context['message'], 'Make sure all fields are entered and valid.')
                self.assertEqual(response.context['error'], True)

        def test_invalid_donor_email_edit(self):
                donation = Donors.objects.create(id = 1, donorFirstName = "John", donorLastName = "Smith", donationAmount = 10, donationDate = '2016-12-08')
                response = self.client.post('/edit_donation/1', {'donorFirstName' : "John", 'donorLastName' : "Smith", 'donorEmail' : 'test',  'donationAmount' : '10.50', 'donationDate' : '2016-12-08'})
                self.assertEqual(response.context['message'], 'Please enter a valid email!')
                self.assertEqual(response.context['error'], True)

	def test_invalid_donation_amount_edit(self):
                donation = Donors.objects.create(id = 1, donorFirstName = "John", donorLastName = "Smith", donationAmount = 10, donationDate = '2016-12-08')
                response = self.client.post('/edit_donation/1', {'donorFirstName' : "John", 'donorLastName' : "Smith", 'donorEmail' : 'testing@gmail.com', 'donationAmount' : '10.50', 'donationDate' : '2016-12-08'})
                self.assertEqual(response.context['message'], 'Please enter donation amount as a whole number')
                self.assertEqual(response.context['error'], True)

        def test_donor_instance(self):
                donor1 = Donors.objects.create(donorFirstName = "Jack",
                                               donorLastName = "Frost",
                                               donationAmount = 10,
                                               donorEmail = "jfrost@gmail.com",
                                               donationDate = '2016-10-02')
                self.assertTrue(isinstance(donor1, Donors))
               

        def test_donor_str(self):
                donor1 = Donors.objects.create(donorFirstName = "Jack",
                                               donorLastName = "Frost",
                                               donationAmount = 10,
                                               donorEmail = "jfrost@gmail.com",
                                               donationDate = '2016-10-02')
                self.assertEqual(donor1.__str__(), donor1.donorFirstName)


class IncidentReportTestCase(TestCase):
	def setUp(self):
		User.objects.create(username="user1", first_name = "Jack", last_name = "Frost", email = "jfrost@gmail.com", password="pass")
		self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		Resident.objects.create(resident_first="first", resident_last="last", date_of_birth="2012-05-23", race="Asian", join_date="2015-02-23")
		
	def test_form_valid(self):
		self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
                data = {'staff': user1,
                        'residents': resident1,
                        'comment': "lol",
                        'activity_type': "Interview",
                        'incident_date': "2010-01-10"}
                form = IncidentForm(data=data)
                self.assertFalse(form.is_valid())
                
	def test_form_invalid_not_all_data(self):
		self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		data = {'staff': user1,
                'residents': resident1,
                'comment': "lol",
                'incident_date': "2010-01-10"}
		form = IncidentForm(data=data)
		self.assertFalse(form.is_valid())
	
	def test_edit_form_exists(self):
		self.user.is_superuser = True
		self.user.save()
		self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post(reverse('incident_report'), {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
		resp = self.client.get(reverse('admin_edit_report', args=[1]))
		self.assertEqual(resp.status_code, 302)

	def test_edit_form_does_not_exist(self):
		self.client.login(username="john", password="johnpassword")
		response = self.client.get('/edit_report/2')
		self.assertRedirects(response, expected_url='/incident_report/', status_code=302, target_status_code = 200)
                
        def test_edit_form_get_not_logged_in(self):
                user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'activity_type' : 'Interview', 'incident_date':'2016-04-24'})
                resp = self.client.get('/edit_report/1')
                self.assertEqual(resp.status_code, 302)
        
#        def test_edit_form_get_staff_logged_in(self):
#                self.client.login(username="john", password="johnpassword")
#                user1 = User.objects.get(username="john")
#		resident1 = Resident.objects.get(resident_first="first")
#		response = self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
#                resp = self.client.get('/edit_report/1')
#                self.assertRedirects(resp, expected_url='/incident_report/', status_code=200, target_status_code = 200)
                
        def test_admin_delete_incident_report(self):
                self.user.is_superuser = True
		self.user.save()
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
                self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
                self.client.get('/delete_report/1')
                response = self.client.get('/incident_report/')
                reports = Incident_Report.objects.all()
                self.assertEqual(len(reports), 0)
        
	def test_admin_delete_incident_report_view(self):
                self.user.is_superuser = True
		self.user.save()
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
                self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
                self.client.get('/delete_report/1')
                response = self.client.get('/incident_report/')
		self.assertNotContains(response, 'TEST')
         
	def test_edit_incident(self):
		self.client.login(username="john", password="johnpassword")
                user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
		response = self.client.post('/edit_report/1', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : '999', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'}, follow=True)
		self.assertContains(response, '999')

	def test_edit_incident_noexist(self):
		self.client.login(username="john", password="johnpassword")
                user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/edit_report/80', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : '999', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
		self.assertEquals(response.status_code, 302)

	def test_edit_incident_noexist2(self):
		self.client.login(username="john", password="johnpassword")
                user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.get('/edit_report/80')
		self.assertEquals(response.status_code, 302)
	

	def test_res_all(self):
		self.client.login(username="john", password="johnpassword") 
		response = self.client.get('/admin_residents_all/')
		self.assertEquals(response.status_code, 200)

	def test_res_curr(self):
		self.client.login(username="john", password="johnpassword") 
		response = self.client.get('/admin_residents_curr/')
		self.assertEquals(response.status_code, 200)

	def test_res_apps(self):
		self.client.login(username="john", password="johnpassword") 
		response = self.client.get('/admin_residents_apps/')
		self.assertEquals(response.status_code, 200)
        
        def test_non_admin_delete_incident_report(self):
                self.client.login(username="john", password="johnpassword")
                user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
                self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
                response = self.client.get('/delete_report/1')
                self.assertRedirects(response, expected_url='/incident_report/', status_code=302, target_status_code = 200)
                
        def test_delete_non_existent_incident_report(self):
                self.user.is_superuser = True
		self.user.save()
                self.client.login(username="john", password="johnpassword")
                response = self.client.get('/delete_report/1')
                self.assertRedirects(response, expected_url='/incident_report/', status_code=302, target_status_code = 200)
                
        def test_delete_report_get_not_logged_in(self):
                user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
                self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'activity_type' : 'Interview', 'incident_date':'2016-04-24'})
                response = self.client.get('/delete_report/1')
                self.assertEqual(response.status_code, 302)
                
                
        def test_edit_form_get_admin_logged_in(self):
                self.user.is_superuser = True
		self.user.save()
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
		resp = self.client.get('/edit_report/1')
                self.assertEqual(resp.status_code, 302)
		

	def test_form_get_not_logged_in(self):
		resp = self.client.get('/incident_report/')
		self.assertEqual(resp.status_code, 302)


	def test_form_get_logged_in(self):
		self.client.login(username="john", password="johnpassword")
		resp = self.client.get('/incident_report/')
		self.assertEqual(resp.status_code, 200)


	def test_form_post_success(self):
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="user1")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/incident_report/', {'staff' : user1, 'residents' : resident1, 'comment' : 'TEST', 'incident_type' : 'NONE', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'}) 

		self.assertEqual(response.status_code, 200)

	def test_form_post_incomplete_data_status(self):
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="user1")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/incident_report/', {'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})

                

		self.assertEqual(response.status_code, 200)

	def test_view_contains_new_report(self):
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="user1")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/incident_report/', {'staff' : user1, 'residents' : resident1, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})

		self.assertContains(response, 'TEST')




	def test_form_post_incident_count(self):
                self.client.login(username="john", password="johnpassword")
		user1 = User.objects.get(username="john")
		resident1 = Resident.objects.get(resident_first="first")
		response = self.client.post('/incident_report/', {'staff' : user1.pk, 'residents' : resident1.pk, 'comment' : 'TEST', 'incident_type' : 'Theft', 'incident_date_0_month':'4', 'incident_date_0_day':'20', 'incident_date_0_year':'2017', 'incident_date_1_hour':'12', 'incident_date_1_minute':'40', 'incident_date_1_second':'50'})
                #print(response)
		self.assertEqual(len(Incident_Report.objects.all()), 0)

class ViewsTestCase(TestCase):
        def test_home(self):
                resp = self.client.get('/')
                self.assertEqual(resp.status_code, 200)
        def test_about(self):
                resp = self.client.get('/about/')
                self.assertEqual(resp.status_code, 200)
        def test_contact(self):
                resp = self.client.get('/contact/')
                self.assertEqual(resp.status_code, 200)
        def test_donate(self):
                resp = self.client.get('/donate/')
                self.assertEqual(resp.status_code, 200)
        def test_gifts(self):
                resp = self.client.get('/gifts/')
                self.assertEqual(resp.status_code, 200)
        def test_donate_online(self):
                resp = self.client.get('/donate_online/')
                self.assertEqual(resp.status_code, 200)
        def test_volunteer(self):
                resp = self.client.get('/volunteer/')
                self.assertEqual(resp.status_code, 200)
        def test_login(self):
                resp = self.client.get('/login/')
                self.assertEqual(resp.status_code, 200)


class AdminStaffTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user2 = User.objects.create_user(username = 'john2', email = 'lennon2@thebeatles.com', password = 'johnpassword2', first_name = "john", last_name = "lennon")
        self.profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
        self.profile2 = UserProfile.objects.create(user = self.user2, user_type = 'STF', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
        self.client.login(username="john", password="johnpassword")
    def test_index(self):
        resp = self.client.get('/admin_staff/')
        self.assertEquals(resp.status_code, 200)
    
    def test_last_name(self):
        resp = self.client.get('/admin_staff/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'lennon')

    def test_first_name(self):
        resp = self.client.get('/admin_staff/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'john')

    def test_email(self):
        resp = self.client.get('/admin_staff/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'lennon2@thebeatles.com')

    def test_status(self):
        resp = self.client.get('/admin_staff/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'True')

    def test_username(self):
        resp = self.client.get('/admin_staff/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'john2')

    def test_last_login(self):
        resp = self.client.get('/admin_staff/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'None')

    def test_add_staff_response(self):
        resp = self.client.get('/admin_add_staff/')
        self.assertEqual(resp.status_code, 200)

class AdminResidentsTestCase(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
                self.user2 = User.objects.create_user(username = 'john2', email = 'lennon2@thebeatles.com', password = 'johnpassword2', first_name = "john", last_name = "lennon")
                self.profile = UserProfile.objects.create(user = self.user, user_type = 'ADM', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
                self.profile2 = UserProfile.objects.create(user = self.user2, user_type = 'STF', user_addr = '123 fake st', user_homeph = '999', user_workph = '777')
                self.client.login(username="john", password="johnpassword")

        def test_admin_residents_last_name(self):
                resp = self.client.get('/admin_residents/')
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, '')

        def test_admin_residents_first_name(self):
                resp = self.client.get('/admin_residents/')
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, '')

        def test_admin_residents_email(self):
                resp = self.client.get('/admin_residents/')
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, '')

        def test_admin_residents_status(self):
                resp = self.client.get('/admin_residents/')
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, '')

        def test_admin_residents_username(self):
                resp = self.client.get('/admin_residents/')
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, '')
                                
                
