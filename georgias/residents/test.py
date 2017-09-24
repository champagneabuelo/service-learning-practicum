""" Unit Tests to Test Code """
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from datetime import datetime as dtdatetime
from .models import Resident, Resident_Application, Resident_Report, Interview_Report, Termination_Report, Meeting_Report, Community_Program, Resident_Employment
from .views import demo
from .forms import ResidentForm, TerminationForm, InterviewForm1, ReportForm
from django.contrib.auth.models import User
from georgias.forms import *
from django.core.management import call_command
from django.contrib.auth import authenticate, login
from django.utils import timezone
import datetime

# Create your tests here.

class FormsTestCase(TestCase):
    def test_resident_form_something(self):
        form_data = {'something':'something'}
        form = ResidentForm(data=form_data)
        self.assertTrue(form.is_valid)

    def test_resident_form_nothing(self):
        form_data = {}
        form = ResidentForm(data=form_data)
        self.assertTrue(form.is_valid)

    def test_termination_form_something(self):
        form_data = {'something':'something'}
        form = TerminationForm(data=form_data)
        self.assertTrue(form.is_valid)

    def test_termination_form_nothing(self):
        form_data = {}
        form = TerminationForm(data=form_data)
        self.assertTrue(form.is_valid)

    def test_interview_form1_something(self):
        form_data = {'something':'something'}
        form = InterviewForm1(data=form_data)
        self.assertTrue(form.is_valid)

    def test_interview_form1_nothing(self):
        form_data = {}
        form = InterviewForm1(data=form_data)
        self.assertTrue(form.is_valid)
        
class ResidentCreationTestCase(TestCase):
    def test_edit_resident(self):
        c = Client()
        c.post('/residents/create/',
               {'resident_first': 'bob',
                'resident_last': 'two',
                'date_of_birth': '2013-04-28',
                'race': 'White'
                })
        apps = Resident_Application.objects.all().count()
        # res = Resident.objects.get(resident_first='bob')
        # c.post('/residents/view_application/{{ res.uniqueid }}', {'approve': True})
        # allres = Resident.objects.all()
        self.assertEqual(apps, 0)
        
class CommunityProgramTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username="john", password="johnpassword")
        Resident.objects.create(resident_first = 'Jack', resident_last = 'Frost', date_of_birth = '1994-02-10', join_date='2014-05-05', race='White', uniqueid="26adfaa3-1a75-47e5-acfa-5fb31423d306",)
        
    def test_community_program_str(self):
        res = Resident.objects.get(resident_first = 'Jack')
        Community_Program.objects.create(resident=res, program_name = "blank", description = "helps with recovering alcohol addicts", uniqueid = "90") 
        Program = Community_Program.objects.get(program_name=u'blank')
        self.assertEqual(Program.__str__(), Program.resident.resident_first)

class EmploymentReportTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username="john", password="johnpassword")
        Resident.objects.create(resident_first = 'Jack', resident_last = 'Frost', date_of_birth = '1994-02-10', join_date='2014-05-05', race='White', uniqueid="26adfaa3-1a75-47e5-acfa-5fb31423d306",)
        
    def test_employment_report_str(self):
        res = Resident.objects.get(resident_first = 'Jack')
        Resident_Employment.objects.create(resident = res, employer = "Sprint", position = "cashier", start_date = "2017-01-01", end_date = "2017-02-02", uniqueid = "3") 
        Report = Resident_Employment.objects.get(employer=u'Sprint')
        self.assertEqual(Report.__str__(), Report.resident.resident_first)
        
class MeetingReportTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username="john", password="johnpassword")
        Resident.objects.create(resident_first = 'Jack', resident_last = 'Frost', date_of_birth = '1994-02-10', join_date='2014-05-05', race='White', uniqueid="26adfaa3-1a75-47e5-acfa-5fb31423d306",)
    
    def test_create_meeting_report(self):
        res = Resident.objects.get(resident_first = 'Jack')
        m = Meeting_Report.objects.create(resident = res, meeting_type = "AA", comment = "adfda", meeting_date = '2010-03-18', uniqueid = "2")
        self.assertEqual(m.resident, res)
        
    def test_rightAssignedMeetingReports(self):
        res = Resident.objects.get(resident_first = 'Jack')
        m = Meeting_Report.objects.create(resident = res, meeting_type = "AA", comment = "adfda", meeting_date = '2010-03-18', uniqueid = "2")
        hasMeetingReport = Resident.objects.get(resident_first=u'Jack')
        Report = Meeting_Report.objects.get(comment=u'adfda')
        self.assertEqual(Report.resident, hasMeetingReport)
        
    def test_meeting_report_str(self):
        res = Resident.objects.get(resident_first = 'Jack')
        Meeting_Report.objects.create(resident = res, meeting_type = "AA", comment = "adfda", meeting_date = '2010-03-18', uniqueid = "2") 
        Report = Meeting_Report.objects.get(comment=u'adfda')
        self.assertEqual(Report.__str__(), Report.resident.resident_first)
        

class ResidentMonthlyReportTestCase(TestCase):
    def setUp(self):
        """ sets up the environment, creates new residents in the interview management page """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username="john", password="johnpassword")
        Resident.objects.create(resident_first = 'Jack', resident_last = 'Frost', date_of_birth = '1994-02-10', join_date='2014-05-05', race='White', uniqueid="26adfaa3-1a75-47e5-acfa-5fb31423d306",)
        Resident.objects.create(resident_first = 'John', resident_last = 'Doe', date_of_birth = '1994-02-10', join_date='2014-05-05', race='Black', uniqueid="2e980140-cfaf-4448-ade9-4fa144f76e56",)
        Resident.objects.create(resident_first = 'Mary', resident_last = 'Smith', date_of_birth = '1994-02-10', join_date='2014-05-05', race='Asian', uniqueid= "2e580140-cfaf-4448-ade9-4fa144f76e56",)
    
    def test_number_of_meeting_reports(self):
        res = Resident.objects.get(resident_first = 'Jack')
        Meeting_Report.objects.create(resident = res, meeting_type = "AA", comment = "adfda", meeting_date = '2010-03-18', uniqueid = "2")
        meetings = Meeting_Report.objects.all().count()
        self.assertEqual(meetings, 1)
        
    def test_number_of_employment_reports(self):
        res = Resident.objects.get(resident_first = 'Jack')
        Resident_Employment.objects.create(resident = res, employer = "Sprint", position = "cashier", start_date = "2017-01-01", end_date = "2017-02-02", uniqueid = "3")
        emp = Resident_Employment.objects.all().count()
        self.assertEqual(emp, 1)
        
    def test_number_of_community_programs(self):
        res = Resident.objects.get(resident_first = 'Jack')
        Community_Program.objects.create(resident=res, program_name = "blank", description = "helps with recovering alcohol addicts", uniqueid = "90")
        com = Community_Program.objects.all().count()
        self.assertEqual(com, 1)
        


class ResidentViewsTestCase(TestCase):
    fixtures = ['ml4zz_fixture.json']
    def setUp(self):
        """ sets up the environment, creates new residents in the interview management page """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username="john", password="johnpassword")
        Resident.objects.create(resident_first = 'Jack', resident_last = 'Frost', date_of_birth = '1994-02-10', join_date='2014-05-05', race='White', uniqueid="26adfaa3-1a75-47e5-acfa-5fb31423d306",)
        Resident.objects.create(resident_first = 'John', resident_last = 'Doe', date_of_birth = '1994-02-10', join_date='2014-05-05', race='Black', uniqueid="2e980140-cfaf-4448-ade9-4fa144f76e56",)
        Resident.objects.create(resident_first = 'Mary', resident_last = 'Smith', date_of_birth = '1994-02-10', join_date='2014-05-05', race='Asian', uniqueid= "2e580140-cfaf-4448-ade9-4fa144f76e56",)


    def test_index(self):
        resp = self.client.get(reverse('resident_home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resident_home.html')

    def test_ind_reports(self):
        resp = self.client.get(reverse('resident_reports'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resident_individual_reports.html')

    def test_ind_monthly_reports(self):
        res =  Resident.objects.get(resident_last=u'One')
        resp = self.client.get(reverse('resident_monthlyReports', args=(res.uniqueid,)))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resident_viewMonthlyReports.html')

    def test_reports_view(self):
        res = Resident.objects.get(resident_last=u'One')
        resp = self.client.get(reverse('reports_view', args=(res.uniqueid,)))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resident_viewReports.html')

    def test_res_manage(self):
        resp = self.client.get(reverse('resident_manage'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resident_manage.html')

    def test_resident_manage_delPost(self):
        res = Resident.objects.get(resident_last=u'One')
        resp = self.client.post('/residents/manage/', {
            'delete 7d931e99-9eb9-469e-96aa-3ad697553b87': u'delete 7d931e99-9eb9-469e-96aa-3ad697553b87'
        })
        self.assertEqual(resp.status_code, 200)

    def test_res_dem(self):
        resp = self.client.get(reverse('demographics'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resident_demographics.html')

    def test_create(self):
        resp = self.client.get(reverse('resident_create'))
        self.assertEqual(resp.status_code, 200)

    def test_manage_termination(self):
        url = reverse('manage_termination')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_edit_residents(self):
        resp = self.client.get('/residents/edit_resident/7d931e99-9eb9-469e-96aa-3ad697553b87')
        self.assertEqual(resp.status_code, 200)

    def test_add_meeting(self):
        resp = self.client.get('/residents/add_meeting/7d931e99-9eb9-469e-96aa-3ad697553b87')
        self.assertEqual(resp.status_code, 200)

    def test_add_meeting_post(self):
        mr = Meeting_Report.objects.get(comment=u'asdf')
        resp = self.client.post('/residents/add_meeting/7d931e99-9eb9-469e-96aa-3ad697553b87', {
            'meeting_type': mr.meeting_type,
            'comment': mr.comment,
            'meeting_date': mr.meeting_date
        })
        self.assertEqual(resp.status_code, 302)




    def test_add_community_program_post(self):
        cp = Community_Program.objects.get(description=u'asdf')
        resp = self.client.post('/residents/add_program/7d931e99-9eb9-469e-96aa-3ad697553b87',{
            'program_name': cp.program_name,
            'description': cp.description
        })
        self.assertEqual(resp.status_code, 302)

    def test_add_community_program(self):
        resp = self.client.get('/residents/add_program/7d931e99-9eb9-469e-96aa-3ad697553b87')
        self.assertEqual(resp.status_code, 200)

    def test_view_monthly_reports_post(self): # pragma: no cover
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp = self.client.post('/residents/view_monthlyReports/7d931e99-9eb9-469e-96aa-3ad697553b87', {
            'month': res.date_of_birth
        })
        self.assertEqual(resp.status_code, 200)

	def test_add_employment(self):# pragma: no cover
		test = '7d931e99-9eb9-469e-96aa-3ad697553b87'
		resp = self.client.get(reverse('add_employment', args=(test,)))
		self.assertEqual(resp.status_code, 200)

    def test_add_employment_post(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp = self.client.post('/residents/add_employment/7d931e99-9eb9-469e-96aa-3ad697553b87', {
            'employer': res.resident_first,
            'position': res.resident_last,
            'start_date': res.date_of_birth,
            'end_date': res.date_of_birth
        })


    def test_view_report(self):
        resp = self.client.get('/residents/view_report/7d931e99-9eb9-469e-96aa-3ad697553b87')
        self.assertEqual(resp.status_code, 200)



    def test_termination_post0(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp=self.client.post('/residents/termination/7d931e99-9eb9-469e-96aa-3ad697553b87/1',{
            'date': res.date_of_birth,
            'reason': res.resident_first
        })
        self.assertEqual(resp.status_code, 200)

    def test_termination_post1(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp = self.client.post('/residents/termination/7d931e99-9eb9-469e-96aa-3ad697553b87/1', {
            'date': res.date_of_birth,
            'reason': res.resident_first
        })
        self.assertEqual(resp.status_code, 200)

    def test_termination_post2(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp = self.client.post('/residents/termination/7d931e99-9eb9-469e-96aa-3ad697553b87/1', {
            'date': res.date_of_birth,
            'reason': res.resident_first
        })
        self.assertEqual(resp.status_code, 200)

    def test_termination_post_notValid(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp = self.client.post('/residents/termination/7d931e99-9eb9-469e-96aa-3ad697553b87/2')
        self.assertEqual(resp.status_code, 200)

    def test_view_interview(self):
        resp = self.client.get('/residents/interview_manage/7d931e99-9eb9-469e-96aa-3ad697553b87')
        self.assertEqual(resp.status_code, 200)

    def test_view_interview_post(self):
        resp = self.client.post('/residents/interview_manage/7d931e99-9eb9-469e-96aa-3ad697553b87',{
            'delete 7d931e99-9eb9-469e-96aa-3ad697553b87': u'delete 7d931e99-9eb9-469e-96aa-3ad697553b87'
        })
        self.assertEqual(resp.status_code, 200)

    def test_view_application(self):
        resp = self.client.get('/residents/view_application/354a5f36-d80b-486a-8a24-556c9ba81190')
        self.assertEqual(resp.status_code, 200)

    def test_view_application_approve(self):
        resp = self.client.post('/residents/view_application/354a5f36-d80b-486a-8a24-556c9ba81190', {
            'approve': u'approve'
        })
        self.assertEqual(resp.status_code, 200)

    def test_view_application_decline(self):
        resp = self.client.post('/residents/view_application/354a5f36-d80b-486a-8a24-556c9ba81190', {
            'decline': u'decline'
        })
        self.assertEqual(resp.status_code, 200)

    def test_add_report(self):
        resp = self.client.get('/residents/add_report/7d931e99-9eb9-469e-96aa-3ad697553b87')
        self.assertEqual(resp.status_code, 200)

    def test_add_report_post(self):
        r = Resident_Report.objects.get(comment=u'a')
        rf = ReportForm({
            'activity_type': r.activity_type,
            'comment': r.comment,
            'date_added': r.date_added
        })
        self.assertTrue(rf.is_valid())
        resp = self.client.post('/residents/add_report/7d931e99-9eb9-469e-96aa-3ad697553b87', {
            'activity_type': r.activity_type,
            'comment': r.comment,
            'date_added': r.date_added
        })
        self.assertEqual(resp.status_code, 200)


    def test_edit_report(self):
        resp = self.client.get('/residents/edit_report/a9d47436-bae3-40d0-9ecd-cd0697c5e677')
        self.assertTrue(resp.status_code, 200)

    def test_edit_report_post(self):
        r = Resident_Report.objects.get(comment=u'a')
        resp = self.client.post('/residents/edit_report/a9d47436-bae3-40d0-9ecd-cd0697c5e677', {
            'activity_type': r.activity_type,
            'comment': r.comment,
            'date_added': r.date_added
        })
        self.assertEqual(resp.status_code, 200)


    def test_res_applications(self):
        resp = self.client.get('/residents/applications/')
        self.assertEqual(resp.status_code, 200)


    def test_termination(self):
        resp = self.client.get('/residents/termination/7d931e99-9eb9-469e-96aa-3ad697553b87/1')
        self.assertEqual(resp.status_code, 200)


    def test_monthlyReports_post_unused(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        resp = self.client.post('/residents/view_monthlyReports/7d931e99-9eb9-469e-96aa-3ad697553b87', {
            'month': res.date_of_birth
        })
        self.assertEqual(resp.status_code, 200) # pragma: no cover


    def test_edit_residents_post(self):
        res = Resident_Application.objects.get(resident_last=u'Two')
        form = ResidentForm({
            'resident_first': res.resident_first,
            'resident_last': res.resident_last,
            'date_of_birth': res.date_of_birth,
            'phone_number': res.phone_number,
            'mailing_address': res.mailing_address,
            'physical_address': res.physical_address,
            'length_at_phys_addr': res.length_at_phys_addr,
            'race': res.race,
            'has_children': res.has_children,
            'has_custody': res.has_custody,
            'is_married_or_relationship': res.is_married_or_relationship,
            'spouse_name': res.spouse_name,
            'spouse_age': res.spouse_age,
            'level_of_education': res.level_of_education,
            'ever_been_to_aa_na': res.ever_been_to_aa_na,
            'aa_or_na': res.aa_or_na,
            'currently_in_aa_na': res.currently_in_aa_na,
            'last_aa_na_meeting': res.last_aa_na_meeting,
            'currently_smokes': res.currently_smokes,
            'willing_to_quit': res.willing_to_quit,
            'has_been_homeless': res.has_been_homeless,
            'has_attempted_suicide': res.has_attempted_suicide,
            'has_experienced_dom_violence': res.has_experienced_dom_violence,
            'has_been_incarcerated': res.has_been_incarcerated,
            'number_of_incar': res.number_of_incar,
            'currently_incar': res.currently_incar,
            'on_probation': res.on_probation,
            'what_ghh_can_provide': res.what_ghh_can_provide,
            'benefits_from_residency': res.benefits_from_residency,
            'goals_in_months': res.goals_in_months,
            'obstacles_for_goals': res.obstacles_for_goals,
            'applicant_attributes': res.applicant_attributes,
            'applicant_essay': res.applicant_essay
        })

        self.assertTrue(form.is_bound)
        resp = self.client.post('/residents/edit_resident/7d931e99-9eb9-469e-96aa-3ad697553b87', {
            'resident_first' : res.resident_first,
            'resident_last' : res.resident_last,
            'date_of_birth' : res.date_of_birth,
            'phone_number': res.phone_number,
            'mailing_address': res.mailing_address,
            'physical_address': res.physical_address,
            'length_at_phys_addr': res.length_at_phys_addr,
            'race': res.race,
            'has_children': res.has_children,
            'has_custody': res.has_custody,
            'is_married_or_relationship': res.is_married_or_relationship,
            'spouse_name': res.spouse_name,
            'spouse_age': res.spouse_age,
            'level_of_education': res.level_of_education,
            'ever_been_to_aa_na': res.ever_been_to_aa_na,
            'aa_or_na': res.aa_or_na,
            'currently_in_aa_na': res.currently_in_aa_na,
            'last_aa_na_meeting': res.last_aa_na_meeting,
            'currently_smokes': res.currently_smokes,
            'willing_to_quit': res.willing_to_quit,
            'has_been_homeless': res.has_been_homeless,
            'has_attempted_suicide': res.has_attempted_suicide,
            'has_experienced_dom_violence': res.has_experienced_dom_violence,
            'has_been_incarcerated': res.has_been_incarcerated,
            'number_of_incar': res.number_of_incar,
            'currently_incar': res.currently_incar,
            'on_probation': res.on_probation,
            'what_ghh_can_provide': res.what_ghh_can_provide,
            'benefits_from_residency': res.benefits_from_residency,
            'goals_in_months': res.goals_in_months,
            'obstacles_for_goals': res.obstacles_for_goals,
            'applicant_attributes': res.applicant_attributes,
            'applicant_essay': res.applicant_essay
        })
        self.assertEqual(resp.status_code, 200)

    def test_p_create(self):
        self.client = Client()
        self.user = User.objects.create_user('john2', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username="john2", password="johnpassword")
        res = Resident_Application.objects.get(resident_last=u'Two')
        form = ResidentForm({
            'resident_first': res.resident_first,
            'resident_last': res.resident_last,
            'date_of_birth': res.date_of_birth,
            'phone_number': res.phone_number,
            'mailing_address': res.mailing_address,
            'physical_address': res.physical_address,
            'length_at_phys_addr': res.length_at_phys_addr,
            'race': res.race,
            'has_children': res.has_children,
            'has_custody': res.has_custody,
            'is_married_or_relationship': res.is_married_or_relationship,
            'spouse_name': res.spouse_name,
            'spouse_age': res.spouse_age,
            'level_of_education': res.level_of_education,
            'ever_been_to_aa_na': res.ever_been_to_aa_na,
            'aa_or_na': res.aa_or_na,
            'currently_in_aa_na': res.currently_in_aa_na,
            'last_aa_na_meeting': res.last_aa_na_meeting,
            'currently_smokes': res.currently_smokes,
            'willing_to_quit': res.willing_to_quit,
            'has_been_homeless': res.has_been_homeless,
            'has_attempted_suicide': res.has_attempted_suicide,
            'has_experienced_dom_violence': res.has_experienced_dom_violence,
            'has_been_incarcerated': res.has_been_incarcerated,
            'number_of_incar': res.number_of_incar,
            'currently_incar': res.currently_incar,
            'on_probation': res.on_probation,
            'what_ghh_can_provide': res.what_ghh_can_provide,
            'benefits_from_residency': res.benefits_from_residency,
            'goals_in_months': res.goals_in_months,
            'obstacles_for_goals': res.obstacles_for_goals,
            'applicant_attributes': res.applicant_attributes,
            'applicant_essay': res.applicant_essay
        })

        resp = self.client.post('/residents/create', {
            'resident_first' : res.resident_first,
            'resident_last': res.resident_last,
            'date_of_birth': res.date_of_birth,
            'phone_number': res.phone_number,
            'mailing_address': res.mailing_address,
            'physical_address' : res.physical_address,
            'length_at_phys_addr' : res.length_at_phys_addr,
            'race': res.race,
            'has_children': res.has_children,
            'has_custody': res.has_custody,
            'is_married_or_relationship': res.is_married_or_relationship,
            'spouse_name': res.spouse_name,
            'spouse_age' : res.spouse_age,
            'level_of_education' : res.level_of_education,
            'ever_been_to_aa_na' : res.ever_been_to_aa_na,
            'aa_or_na': res.aa_or_na,
            'currently_in_aa_na': res.currently_in_aa_na,
            'last_aa_na_meeting': res.last_aa_na_meeting,
            'currently_smokes': res.currently_smokes,
            'willing_to_quit': res.willing_to_quit,
            'has_been_homeless': res.has_been_homeless,
            'has_attempted_suicide': res.has_attempted_suicide,
            'has_experienced_dom_violence': res.has_experienced_dom_violence,
            'has_been_incarcerated': res.has_been_incarcerated,
            'number_of_incar': res.number_of_incar,
            'currently_incar': res.currently_incar,
            'on_probation': res.on_probation,
            'what_ghh_can_provide': res.what_ghh_can_provide,
            'benefits_from_residency': res.benefits_from_residency,
            'goals_in_months': res.goals_in_months,
            'obstacles_for_goals': res.obstacles_for_goals,
            'applicant_attributes': res.applicant_attributes,
            'applicant_essay': res.applicant_essay
        })
        self.assertEqual(resp.status_code, 301)

    def test_first_name(self):
        resp = self.client.get(reverse('interview_manage'))
        self.assertEqual(resp.status_code, 200)
        #self.assertContains(resp, 'John')

    def test_last_name(self):
        resp = self.client.get(reverse('interview_manage'))
        self.assertEqual(resp.status_code, 200)
        #self.assertContains(resp, 'Doe')

    def test_post_monthlyReports(self):
        resp = self.client.post('/login/', {'username': 'user1', 'password': 'pass'})

    def test_right_num_residents(self):
        resident_data = Resident.objects.all().count()
        self.assertEqual(resident_data, 5)

    def test_name_working(self):
        res = Resident.objects.get(resident_first = 'Jack')
        self.assertEqual(res.resident_first, 'Jack')

    def test_resident_str(self):
        res = Resident.objects.get(resident_first = 'Jack')
        self.assertEqual(res.__str__(), res.resident_first)


class ReportTestCase(TestCase):
    fixtures = ['ml4zz_fixture.json']

    def test_rightNumResidents(self):
        resident_data = Resident.objects.all().count()
        self.assertEqual(resident_data, 2)

    def test_rightAssignedReports(self):
        hasReport = Resident.objects.get(resident_last=u'One')
        Report = Resident_Report.objects.get(comment=u'a')
        self.assertEqual(Report.resident, hasReport)

    def test_resident_report_str(self):
         Report = Resident_Report.objects.get(comment=u'a')
         self.assertEqual(Report.__str__(), Report.resident.resident_first)

    def test_nameWorking(self):
        resWithLongName = Resident(resident_first=u'aaaaaaaaaaaaaaaaaaaaaaaaaaaa',


                                   resident_last=u'aaaaaaaaaaaaaaaaaaaaaaaaaaaa', date_of_birth=dtdatetime.now(),
                                   join_date=dtdatetime.now(), race='Asian')

        resWithLongName.save()
        self.assertEqual(resWithLongName.resident_first, u'aaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    def test_race_not_limited(self):
        res_race_unknown = Resident(resident_first=u'b', resident_last=u'b', date_of_birth=dtdatetime.now(), join_date=dtdatetime.now(), race='NotAvail')
        res_race_unknown.save()
        self.assertEqual(res_race_unknown.race, 'NotAvail')



    def test_rightNumReports(self):
        report_data = Resident_Report.objects.all().count()
        self.assertEqual(report_data, 1)

    def test_rightNumApplicants(self):
        applicant_data = Resident_Application.objects.all().count()
        self.assertEqual(applicant_data, 4)


    def test_resident_application_str(self):
        applicant = Resident_Application.objects.get(resident_last=u'Two')
        self.assertEqual(applicant.__str__(), applicant.resident_first)

    def test_interview_application(self):
        applicant = Resident_Application.objects.get(resident_last=u'Two')
        int_rep = Interview_Report.objects.get(emergency_contact_name=u'b')
        self.assertEqual(applicant.interview_report, int_rep)

    def test_interview_str(self):
        int_rep = Interview_Report.objects.get(emergency_contact_name=u'b')
        self.assertEqual(int_rep.__str__(), int_rep.comment)

    def test_interview_application_create(self):
        int_rep = Interview_Report(emergency_contact_name=u'b')
        applicant = Resident_Application.objects.get(resident_last=u'One')
        applicant.interview_report = int_rep
        self.assertEqual(applicant.interview_report, int_rep)

# all phone validation tests will be done with reference phone number; phone_number field
# likely to be deprecated in future


    def test_interview_application_phone_number_1(self): # pragma: no cover
        """ testing acceptable entry for phone number"""
        report = Interview_Report(reference_phone=u'7034763997')
        with self.assertRaises(ValidationError):
            if report.full_clean():
                report.save()
        self.assertEqual(
	Interview_Report.objects.filter(reference_phone=u'7034763997').count(), 0
	)

    def test_interview_application_phone_number_2(self): # pragma: no cover
        """testing acceptable entry for phone number"""
        report = Interview_Report(reference_phone=u'703-476-3997')
        with self.assertRaises(ValidationError):
            if report.full_clean():
                report.save()
        self.assertEqual(
	Interview_Report.objects.filter(reference_phone=u'703-476-3997').count(), 0
	)

    def test_interview_application_phone_number_3(self): # pragma: no cover
        """testing acceptable entry for phone number"""
        report = Interview_Report(reference_phone=u'(703) 476-3997')
        with self.assertRaises(ValidationError):
            if report.full_clean():
                report.save()
        self.assertEqual(
	Interview_Report.objects.filter(reference_phone=u'(703) 476-3997').count(), 0
	)

    def test_interview_application_phone_number_4(self): # pragma: no cover
        """testing acceptable entry for phone number"""
        report = Interview_Report(reference_phone=u'476-3997')
        with self.assertRaises(ValidationError):
            if report.full_clean():
                report.save()
        self.assertEqual(
	Interview_Report.objects.filter(reference_phone=u'476-3997').count(), 0
	)

    def test_interview_application_phone_number_5(self): # pragma: no cover
        """testing acceptable entry for phone number"""
        report = Interview_Report(reference_phone=u'(703)4763997')
        with self.assertRaises(ValidationError):
            if report.full_clean():
                report.save()
        self.assertEqual(
	Interview_Report.objects.filter(reference_phone=u'(703)4763997').count(), 0
	)

    def test_interview_application_phone_number_6(self): # pragma: no cover
        """testing unacceptable entry for phone number"""
        report = Interview_Report(reference_phone=u'1')
        with self.assertRaises(ValidationError):
            if report.full_clean():
                report.save()
        self.assertEqual(
	Interview_Report.objects.filter(reference_phone=u'1').count(), 0
	)

    def test_count_interviews(self):
        interview_all = Interview_Report.objects.all().count()
        self.assertEqual(interview_all, 2)

    def test_unassigned_report(self):
        interview_reports = Interview_Report.objects.all()
        applicant = Resident_Application.objects.get(resident_last=u'One')
        bool = False
        for interviews in interview_reports:
            if applicant.interview_report == interviews:
                bool = True
        self.assertEqual(bool, True)

    def test_name_assignment(self):
        res1 = Resident.objects.get(resident_last=u'One')
        res2 = Resident.objects.get(resident_last=u'Two')
        bool = False
        if res1.resident_first == u'Resident' and res2.resident_first == u'Resident':
            bool = True
        self.assertEqual(bool, True)

    def test_term_report_fname(self):
        res1 = Resident.objects.get(resident_last=u'One')
        t = Termination_Report(resident_first=res1.resident_first, resident_last=res1.resident_last, reason="aaaa", date=dtdatetime.now())
        self.assertEqual(t.resident_first, res1.resident_first)

    def test_term_report_lname(self):
        res1 = Resident.objects.get(resident_last=u'One')
        t = Termination_Report(resident_first=res1.resident_first, resident_last=res1.resident_last, reason="aaaa", date=dtdatetime.now())
        self.assertEqual(t.resident_last, res1.resident_last)

    def test_term_report_fdel(self):
        res1 = Resident.objects.get(resident_last=u'One')
        holder = res1.resident_first
        t = Termination_Report(resident_first=res1.resident_first, resident_last=res1.resident_last, reason="aaaa", date=dtdatetime.now())
        res1.delete()
        self.assertEqual(t.resident_first, holder)


    def test_term_report_ldel(self):
        res1 = Resident.objects.get(resident_last=u'One')
        holder = res1.resident_last
        t = Termination_Report(resident_first=res1.resident_first, resident_last=res1.resident_last, reason="aaaa", date=dtdatetime.now())
        res1.delete()
        self.assertEqual(t.resident_last, holder)

    def test_term_report_reason(self):
        res1 = Resident.objects.get(resident_last=u'One')
        holder = res1.resident_last

        t = Termination_Report(resident_first=res1.resident_first, resident_last=res1.resident_last, reason="aaaa",

                               date=dtdatetime.now())
        res1.delete()
        self.assertEqual(t.reason, u'aaaa')

    def test_app_term_report_fname(self):
        rep = Resident_Application.objects.get(resident_last=u'One')

        t = Termination_Report(resident_first=rep.resident_first, resident_last=rep.resident_last, reason="aaaa",
                               date=dtdatetime.now())


        self.assertEqual(t.resident_first, rep.resident_first)

    def test_app_term_report_lname(self):
        rep = Resident_Application.objects.get(resident_last=u'One')
        t = Termination_Report(resident_first=rep.resident_first, resident_last=rep.resident_last, reason="aaaa",
                               date=dtdatetime.now())
        self.assertEqual(t.resident_last, rep.resident_last)

    def test_app_term_report_fdel(self):
        rep = Resident_Application.objects.get(resident_last=u'LNAME')
        holder = rep.resident_first
        t = Termination_Report(resident_first=rep.resident_first, resident_last=rep.resident_last, reason="aaaa",
                               date=dtdatetime.now())
        self.assertEqual(t.resident_first, holder)

    def test_app_term_report_ldel(self):
        rep = Resident_Application.objects.get(resident_last=u'LNAME')
        holder = rep.resident_last
        t = Termination_Report(resident_first=rep.resident_first, resident_last=rep.resident_last, reason="aaaa",
                               date=dtdatetime.now())
        self.assertEqual(t.resident_last, holder)

    def test_app_term_report_reason(self):
        rep = Resident_Application.objects.get(resident_last=u'LNAME')
        holder = rep.resident_last
        t = Termination_Report(resident_first=rep.resident_first, resident_last=rep.resident_last, reason="aaaa",
                               date=dtdatetime.now())
        self.assertEqual(t.reason, u'aaaa')

    def test_demographic_init(self):
        dem = demo()
        self.assertEqual(dem.total, 0)
        self.assertEqual(dem.AMAL, 0)
        self.assertEqual(dem.AS, 0)
        self.assertEqual(dem.BL, 0)
        self.assertEqual(dem.HPI, 0)
        self.assertEqual(dem.WH, 0)
        self.assertEqual(dem.HI, 0)
        #self.assertEqual(allZero, True)


    def test_demographic_init_per(self):
        dem = demo()
        self.assertEqual(dem.per_AMAL, 0)
        self.assertEqual(dem.per_AS, 0)
        self.assertEqual(dem.per_BL, 0)
        self.assertEqual(dem.per_HPI, 0)
        self.assertEqual(dem.per_WH, 0)
        self.assertEqual(dem.per_HI, 0)

    def test_demographic_perc_noupdate(self):
        dem = demo()
        dem.inc_WH()
        dem.inc_AS()
        self.assertEqual(dem.per_AS, 0)

    def test_demographic_perc_update(self):
        dem = demo()
        dem.inc_WH()
        dem.inc_AS()
        dem.inc_AMAL()
        dem.inc_HPI()
        dem.inc_HI()
        dem.update_per()
        self.assertEqual(dem.per_AS, 20)

    def test_demographic_total(self):
        dem = demo()
        dem.inc_WH()
        dem.inc_AS()
        dem.inc_BL()
        self.assertEqual(dem.total, 3)

    def test_only_wh_perc(self):
	dem = demo()
	dem.inc_WH()
	dem.inc_WH()
	dem.update_per()
	self.assertEqual(dem.per_WH, 100)
