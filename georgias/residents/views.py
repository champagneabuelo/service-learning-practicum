from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from django.forms.models import model_to_dict
from .models import Resident, Resident_Application, Interview_Report
from georgias.models import Incident_Report
from .models import Resident_Report, Termination_Report, Meeting_Report, Resident_Monthly_Report, Terminated_Resident
from .forms import ResidentForm, ReportForm, InterviewForm, TerminationForm, MeetingForm, ReportForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User, Group
import os
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import forms
from formtools.wizard.views import SessionWizardView
from forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from itertools import chain

# Processing and querying data from the database for each template on the system
# Create your views here.

def index(request): 
    """ display the home page for residents """
    return render(request, 'resident_home.html') 


def resident_reports(request):
    """ Displays active residents to view their reports """
    residents = Resident.objects.filter(validated=1) # list of active residents
    return render(request, 'resident_individual_reports.html', {'residents': residents}) # renders the resident reports main page


def resident_viewMonthlyReports(request, resident_pk): 
    """ Filters resident's reports by month and year """
    form = MonthlyReportForm(label_suffix = "") # form for montlhy report form
    resident = Resident.objects.get(uniqueid=resident_pk) # the resident associated with the report
    if request.method == "POST": # pragma: no cover # if data is being sent
        form = MonthlyReportForm(request.POST, label_suffix="")
        if form.is_valid(): 
            r = Resident_Monthly_Report(
			resident = resident,
			month = form.cleaned_data["month"], 
		) # grabs month and year to filter by from the form
        r.save()
        # resident data is filtered based on the passed in month and year
        aa_meetings = Meeting_Report.objects.filter(meeting_type="Alcoholics Anonymous", meeting_date__month=r.month.month, meeting_date__year = r.month.year, resident=resident) # resident's alcohol anonymous meetings
        na_meetings = Meeting_Report.objects.filter(meeting_type="Narcotics Anonymous", meeting_date__month=r.month.month, meeting_date__year = r.month.year, resident=resident) # resident's narcotics anonyous meetings
        house_meetings = Meeting_Report.objects.filter(meeting_type="House Meeting", meeting_date__month=r.month.month, meeting_date__year = r.month.year, resident=resident) # resident's house meetings
        aa_and_na_count = len(aa_meetings) + len(na_meetings) # total number of aa and na meetings
        house_count = len(house_meetings) # number of house meetings
        programs = Community_Program.objects.filter(resident=resident) # resident's community programs
        employments = Resident_Employment.objects.filter(resident=resident, start_date__month=r.month.month, start_date__year = r.month.year) # resident's employments
        incidents = Incident_Report.objects.filter(residents=resident, incident_date__month = r.month.month, incident_date__year = r.month.year) # resident's incident reports
        incident_count = len(incidents) # number of incident reports
        meetings = Meeting_Report.objects.filter(resident=resident, meeting_date__month = r.month.month, meeting_date__year = r.month.year) # resident's meetings
        reports = Resident_Report.objects.filter(resident=resident, date_added__month = r.month.month, date_added__year = r.month.year)
        return render(request, 'resident_viewMonthlyReports.html', {'form': form, 'resident': resident, 'incidents': incidents, 'incident_count': incident_count, 'aa_and_na_count' : aa_and_na_count, 'house_count': house_count, 'meetings': meetings, 'employments' : employments, 'programs': programs, 'reports' : reports}) # render monthly report form page and pass data
    return render(request, 'resident_viewMonthlyReports.html', {'resident': resident, 'form': form}) # if no data is being sent, just display the form

def resident_viewReports(request, resident_pk):
    """ Display all of resident's reports """
    resident = Resident.objects.get(uniqueid=resident_pk)
    incidents = Incident_Report.objects.filter(residents=resident)
    incident_count = len(incidents)
    meetings = Meeting_Report.objects.filter(resident=resident)
    aa_meetings = Meeting_Report.objects.filter(resident=resident, meeting_type="Alcoholics Anonymous")
    na_meetings = Meeting_Report.objects.filter(resident=resident, meeting_type="Narcotics Anonymous")
    house_meetings = Meeting_Report.objects.filter(resident=resident, meeting_type="House Meeting")
    aa_and_na_count = len(aa_meetings) + len(na_meetings)
    house_count = len(house_meetings)
    form = MeetingForm(label_suffix = "")
    programs = Community_Program.objects.filter(resident=resident)
    employments = Resident_Employment.objects.filter(resident=resident)
    reports = Resident_Report.objects.filter(resident=resident)
    return render(request, 'resident_viewReports.html', {'resident': resident, 'incidents': incidents, 'incident_count': incident_count, 'form':form, 'aa_and_na_count' : aa_and_na_count, 'house_count': house_count, 'meetings': meetings, 'employments' : employments, 'programs': programs, 'reports': reports})
    
    
def resident_addMeeting(request, resident_pk): 
    """ Add a meeting for a resident """
    form = MeetingForm(label_suffix="")
    resident = Resident.objects.get(uniqueid=resident_pk)
    if request.method == "POST": # retrieve data
        form = MeetingForm(request.POST, label_suffix="")
        if form.is_valid(): # if all fields filled out correctly
            m = Meeting_Report(
			resident = resident,
			meeting_type = form.cleaned_data["meeting_type"],
			comment = form.cleaned_data["comment"],
			meeting_date = form.cleaned_data["meeting_date"]
		) # set up the new meeting report object from the passed in data
            m.save() # save meeting into database
            return redirect(reverse('reports_view', kwargs={'resident_pk':resident_pk})) # return to the resident's reports page
    else : # display the form
        form = MeetingForm(label_suffix="")
        return render(request, 'resident_addMeeting.html', {
                'form':form,
                'resident':resident,
        }) # display the template and the data
    
def resident_addProgram(request, resident_pk): 
    """ add a community program report for a resident """
    form = CommunityProgramForm(label_suffix="")
    resident = Resident.objects.get(uniqueid=resident_pk)
    if request.method == "POST": # data has been sent
        form = CommunityProgramForm(request.POST, label_suffix="")
        if form.is_valid(): # if all fields filled out correctly
            p = Community_Program(
			resident = resident,
			program_name = form.cleaned_data["program_name"], 
			description = form.cleaned_data["description"]
		) # set up the new community program object from the passed in data
            p.save() # save community program
            return redirect(reverse('reports_view', kwargs={'resident_pk':resident_pk})) # return to the resident's reports page
    else :
        form = CommunityProgramForm(label_suffix="")
        return render(request, 'resident_addProgram.html', {
                'form':form,
                'resident':resident,
        }) # display the template and data
    
def resident_addEmployment(request, resident_pk): 
    """ add an employment program report for a resident """
    form = EmploymentForm(label_suffix="")
    resident = Resident.objects.get(uniqueid=resident_pk)
    if request.method == "POST": # data has been sent
        form = EmploymentForm(request.POST, label_suffix="")
        if form.is_valid(): # if valid parse data
            e = Resident_Employment(
			resident = resident,
			employer = form.cleaned_data["employer"],
			position = form.cleaned_data["position"],
			start_date = form.cleaned_data["start_date"],
			end_date = form.cleaned_data["end_date"]
		) # set up resident employment object with passed in data
            e.save() # save resident employment
            return redirect(reverse('reports_view', kwargs={'resident_pk':resident_pk})) # return to resident's reports page
    else : # pragma: no cover
        form = EmploymentForm(label_suffix="")
        return render(request, 'resident_addEmployment.html', {
                'form':form,
                'resident':resident,
        }) # display the template and data


def resident_add(request): 
    """ add a resident """
    if request.method == "GET": #
        form = ResidentForm()
        return render( request, 'resident_create.html', {
            'form': form,
        } ) # display template and form
    elif request.method == "POST": # data has been sent
        form = ResidentForm(request.POST, request.FILES)
        if form.is_valid(): # pragma: no cover # if valid then parse data
            resident_first = form.cleaned_data["resident_first"]
            resident_last = form.cleaned_data["resident_last"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            phone_number = form.cleaned_data["phone_number"]
            mailing_address = form.cleaned_data["mailing_address"]
            physical_address = form.cleaned_data["physical_address"]
            length_at_phys_addr = form.cleaned_data["length_at_phys_addr"]
            race = form.cleaned_data["race"]
            has_children = form.cleaned_data["has_children"]
            has_custody = form.cleaned_data["has_custody"]
            is_married_or_relationship = form.cleaned_data["is_married_or_relationship"]
            spouse_name = form.cleaned_data["spouse_name"]
            spouse_age = form.cleaned_data["spouse_age"]
            level_of_education = form.cleaned_data["level_of_education"]
            ever_been_to_aa_na = form.cleaned_data["ever_been_to_aa_na"]
            aa_or_na = form.cleaned_data["aa_or_na"]
            currently_in_aa_na = form.cleaned_data["currently_in_aa_na"]
            last_aa_na_meeting = form.cleaned_data["last_aa_na_meeting"]
            currently_smokes = form.cleaned_data["currently_smokes"]
            willing_to_quit = form.cleaned_data["willing_to_quit"]
            has_been_homeless = form.cleaned_data["has_been_homeless"]
            has_attempted_suicide = form.cleaned_data["has_attempted_suicide"]
            has_experienced_dom_violence = form.cleaned_data["has_experienced_dom_violence"]
            has_been_incarcerated = form.cleaned_data["has_been_incarcerated"]
            number_of_incar = form.cleaned_data["number_of_incar"]
            currently_incar = form.cleaned_data["currently_incar"]
            on_probation = form.cleaned_data["on_probation"]
            what_ghh_can_provide = form.cleaned_data["what_ghh_can_provide"]
            benefits_from_residency = form.cleaned_data["benefits_from_residency"]
            goals_in_months = form.cleaned_data["goals_in_months"]
            obstacles_for_goals = form.cleaned_data["obstacles_for_goals"]
            applicant_attributes = form.cleaned_data["applicant_attributes"]
            applicant_essay = form.cleaned_data["applicant_essay"]
            rep = Resident_Application(phone_number=phone_number, resident_first=resident_first, resident_last=resident_last, date_of_birth=date_of_birth, race=race, mailing_address=mailing_address, physical_address=physical_address, length_at_phys_addr=length_at_phys_addr, has_children=has_children, has_custody=has_custody, is_married_or_relationship=is_married_or_relationship, spouse_name=spouse_name, spouse_age=spouse_age, level_of_education=level_of_education, ever_been_to_aa_na=ever_been_to_aa_na, aa_or_na=aa_or_na, currently_in_aa_na=currently_in_aa_na, last_aa_na_meeting=last_aa_na_meeting, currently_smokes=currently_smokes, willing_to_quit=willing_to_quit, has_been_homeless=has_been_homeless, has_attempted_suicide=has_attempted_suicide, has_experienced_dom_violence=has_experienced_dom_violence, has_been_incarcerated=has_been_incarcerated, number_of_incar=number_of_incar, currently_incar=currently_incar, on_probation=on_probation, what_ghh_can_provide=what_ghh_can_provide, benefits_from_residency=benefits_from_residency, goals_in_months=goals_in_months, obstacles_for_goals=obstacles_for_goals, applicant_attributes=applicant_attributes, applicant_essay=applicant_essay)
            rep.save() # save resident form
            resident_apps = Resident_Application.objects.filter(interview_report=None)
            return render(request, 'resident_applications.html', {
                'resident_apps': resident_apps
            }) # go to resident applicants page and display applications
        else:
            return render( request, 'resident_create.html', {
                'form': form,
            }) # go back to application form page

    
def resident_manage(request):
    """ Display all active residents """
    resident_data = Resident.objects.filter(validated=1)
    for resident in resident_data:
        if request.POST.get("delete " + str(resident.uniqueid)):
            resident.delete()
            resident_data = Resident.objects.all()
    return render(request, 'resident_manage.html', {
        'resident_data': resident_data,
    })

def resident_manage_termination(request):
    """ Display all terminated residents """
    #termination_data_0 = Termination_Report.objects.filter(phase=u'Pre-Interview')
    #termination_data_1 = Termination_Report.objects.filter(phase=u'Post-Interview')
    #termination_data_2 = Termination_Report.objects.filter(phase=u'Residency')
    #termination_data_3 = Termination_Report.objects.filter(phase=u'Graduation')
    term_data_0 = Termination_Report.objects.filter(phase=u'Pre-Interview')
    term_data_1 = Termination_Report.objects.filter(phase=u'Post-Interview')
    term_data_2 = Terminated_Resident.objects.filter(phase=u'Residency')
    term_data_3 = Terminated_Resident.objects.filter(phase=u'Graduation')
    return render(request, 'resident_manage_termination.html', {
        'data_0': term_data_0,
        'data_1': term_data_1,
        'data_2': term_data_2,
        'data_3': term_data_3
    })

def resident_manage_interview(request):
    """ Display all interviewed applicants """
    resident_interviews = Resident.objects.filter(validated=0).exclude(interview_report_id=None)
    return render(request, 'resident_manage_interview.html',{
        'data': resident_interviews
    })




def edit_resident(request, resident_pk):
    """ Edit resident application information """
    resident = Resident.objects.get(uniqueid=resident_pk)
    resident_application = Resident_Application.objects.get(interview_report=resident.interview_report)
    if request.method == "GET":
        form = ResidentForm(instance=resident_application)
#        form.fields['comments'].widget = forms.HiddenInput()
        return render(request, 'resident_edit.html', {
            'form': form,
            'resident': resident_application,
        })
        #print("get request - show filled out form with data")
    elif request.method == "POST":
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid(): # pragma: no cover
            form.save()
            resident.resident_first = form.cleaned_data["resident_first"]
            resident_application.resident_first = form.cleaned_data["resident_first"]
            resident.resident_last = form.cleaned_data["resident_last"]
            resident_application.resident_last = form.cleaned_data["resident_last"]
            resident.date_of_birth = form.cleaned_data["date_of_birth"]
            resident_application.date_of_birth = form.cleaned_data["date_of_birth"]


            resident_application.phone_number = form.cleaned_data["phone_number"]
            resident_application.mailing_address = form.cleaned_data["mailing_address"]
            resident_application.physical_address = form.cleaned_data["physical_address"]
            resident_application.length_at_phys_addr = form.cleaned_data["length_at_phys_addr"]
            resident_application.race = form.cleaned_data["race"]
            resident_application.has_children = form.cleaned_data["has_children"]
            resident_application.has_custody = form.cleaned_data["has_custody"]
            resident_application.is_married_or_relationship = form.cleaned_data["is_married_or_relationship"]
            resident_application.spouse_name = form.cleaned_data["spouse_name"]
            resident_application.spouse_age = form.cleaned_data["spouse_age"]
            resident_application.level_of_education = form.cleaned_data["level_of_education"]
            resident_application.ever_been_to_aa_na = form.cleaned_data["ever_been_to_aa_na"]
            resident_application.aa_or_na = form.cleaned_data["aa_or_na"]
            resident_application.currently_in_aa_na = form.cleaned_data["currently_in_aa_na"]
            resident_application.last_aa_na_meeting = form.cleaned_data["last_aa_na_meeting"]
            resident_application.currently_smokes = form.cleaned_data["currently_smokes"]
            resident_application.willing_to_quit = form.cleaned_data["willing_to_quit"]
            resident_application.has_been_homeless = form.cleaned_data["has_been_homeless"]
            resident_application.has_attempted_suicide = form.cleaned_data["has_attempted_suicide"]
            resident_application.has_experienced_dom_violence = form.cleaned_data["has_experienced_dom_violence"]
            resident_application.has_been_incarcerated = form.cleaned_data["has_been_incarcerated"]
            resident_application.number_of_incar = form.cleaned_data["number_of_incar"]
            resident_application.currently_incar = form.cleaned_data["currently_incar"]
            resident_application.on_probation = form.cleaned_data["on_probation"]
            resident_application.what_ghh_can_provide = form.cleaned_data["what_ghh_can_provide"]
            resident_application.benefits_from_residency = form.cleaned_data["benefits_from_residency"]
            resident_application.goals_in_months = form.cleaned_data["goals_in_months"]
            resident_application.obstacles_for_goals = form.cleaned_data["obstacles_for_goals"]
            resident_application.applicant_attributes = form.cleaned_data["applicant_attributes"]
            resident_application.applicant_essay = form.cleaned_data["applicant_essay"]
            resident.save()
            resident_application.save()
        resident_data = Resident.objects.all()
        return render(request, 'resident_manage.html', {
            'resident_data': resident_data,
        })
       



def resident_applications(request):
    """ Displays all resident applications """
    resident_apps = Resident_Application.objects.filter(interview_report=None)
    return render(request, 'resident_applications.html', {
        'resident_apps': resident_apps
    })

# Using form wizard here for multi-page form
named_interview_forms = (
	('page_1', InterviewForm1),
	('page_2', InterviewForm2),
	('page_3', InterviewForm3),
	('page_4', InterviewForm4),
	('page_5', InterviewForm5),
	('page_6', InterviewForm6),
	('page_7', InterviewForm7),
)

templates = {
	'page_1': 'interview_form_1.html',
	'page_2': 'interview_form_2.html',
	'page_3': 'interview_form_3.html',
	'page_4': 'interview_form_4.html',
	'page_5': 'interview_form_5.html',
	'page_6': 'interview_form_6.html',
	'page_7': 'interview_form_7.html'
}

class resident_interviewForm(SessionWizardView):
        """ Displays form for interview form """
	instance = None
	def get_form_instance(self, step): #pragma: no cover
		if self.instance is None:
			self.instance = Interview_Report()
		return self.instance
	
	def get_template_names(self): #pragma: no cover
		return [templates[self.steps.current]]

	def done(self, form_list, form_dict, **kwargs): #pragma: no cover
		form_list = kwargs.pop('form_list', form_list)
		form_dict = kwargs.pop('form_dict', form_dict)	
		for key in kwargs:
			resident = Resident_Application.objects.get(uniqueid=kwargs[key])
			form = self.instance
			form.save()

			resident.interview_report = form
			resident.save()
			new_resident = Resident(
				resident_first=resident.resident_first, 
				resident_last=resident.resident_last, 
				date_of_birth=resident.date_of_birth, 
				join_date=datetime.datetime.now(), 
				race=resident.race, 
				interview_report=resident.interview_report, 
				validated = 0
			)
 			new_resident.save()
		return redirect(reverse('interview_manage'))

wizard_view = resident_interviewForm.as_view(named_interview_forms)

def wrapped_interview_form(request, resident_pk): #pragma: no cover
	return wizard_view(request, pk=resident_pk)    

def resident_reportsViewInterview(request, resident_pk): # pragma: no cover
    """ Display interview for residents reports page """
    resident = Resident.objects.get(uniqueid=resident_pk)
    #data = resident.interview_report._meta.get_fields()
    data = resident.interview_report.get_all_int_fields()
    if request.method == "GET":
        return render(request, 'resident_reportsViewInterview.html', {
            'resident': resident,
            'form': data
        })

def resident_viewInterview(request, resident_pk):
    """ Display all fields for resident's interview form and allows for interviewee termination or approval for residency """
    resident = Resident.objects.get(uniqueid=resident_pk)
    #data = resident.interview_report._meta.get_fields()
    data = resident.interview_report.get_all_int_fields()
    if request.method == "GET":
        return render(request, 'resident_viewInterview.html', {
            'resident': resident,
            'form': data
        })
    elif request.method == "POST":
        resident.validated = 1
        resident.save()
        resident_data = Resident.objects.filter(validated=1)
        for resident in resident_data:
            if request.POST.get("delete " + str(resident.uniqueid)):
                resident.delete()
                resident_data = Resident.objects.all()
        return render(request, 'resident_manage.html', {
            'resident_data': resident_data,
        })




def resident_viewApplication(request, resident_pk):
    """ Display all fields for resident's applications and allows for application termination or approval """
    resident = Resident_Application.objects.get(uniqueid=resident_pk)
    res_model = ResidentForm(data=model_to_dict(Resident_Application.objects.get(uniqueid=resident_pk)))
    #data = resident.application_form.get_all_int_fields()
    if request.method == "GET":
        return render(request, 'resident_viewApplication.html', {
            'resident': resident,
            'res_model': res_model
        })
    elif request.method == "POST":
        if request.POST.get("approve") != None:
            resident_first = resident.resident_first
            resident_last = resident.resident_last
            interview_report = resident.interview_report
            date_of_birth = resident.date_of_birth
            race = resident.race
            join_date = timezone.now()
            r = Resident(resident_first=resident_first, resident_last=resident_last, date_of_birth=date_of_birth, join_date=join_date, interview_report=interview_report, race=race)
            r.save()
            resident.delete()
            resident_data = Resident.objects.all()
            return render(request, 'resident_manage.html', {
                'resident_data': resident_data,
            })
        elif request.POST.get("decline") != None:
            resident.delete()
            resident_apps = Resident_Application.objects.all()
            return render(request, 'resident_applications.html', {
                'resident_apps': resident_apps
            })
        
def resident_reportsViewApplication(request, resident_pk):# pragma: no cover
    """ Display all fields for application on the resident's reports page """
    resident = Resident.objects.get(uniqueid=resident_pk)
    res_model = ResidentForm(data=model_to_dict(Resident_Application.objects.get(resident_first = resident.resident_first, resident_last=resident.resident_last)))
    
    if request.method == "GET":
        return render(request, 'resident_reportsViewApplication.html', {
            'resident': resident,
            'res_model' : res_model
        })
    

def resident_termination(request, resident_pk, phase_pk):
    resident = ""
    if phase_pk == u'0': # pragma: no cover
        resident = Resident_Application.objects.get(uniqueid=resident_pk)
    elif phase_pk == u'1' or phase_pk == u'2' or phase_pk == u'3':
        resident = Resident.objects.get(uniqueid=resident_pk)
    """ Terminates resident based on the passed in resident primary key and saves the phase the resident is terminated in """
    if request.method == "POST":
        form = TerminationForm(request.POST, label_suffix="")
        if form.is_valid():
            res_first = resident.resident_first
            res_last = resident.resident_last
            phase = "" # which phase the resident is terminated in
            if phase_pk == u'0': # pragma : no cover
                phase = "Pre-Interview"
            elif phase_pk == u'1':
                phase = "Post-Interview"
            elif phase_pk == u'2': # pragma: no cover
                phase = "Residency"
                t_res = Terminated_Resident(resident=resident, resident_first=res_first, resident_last=res_last, date=form.cleaned_data["date"], reason=form.cleaned_data['reason'], phase=phase, race=resident.race)
                t_res.save()
            elif phase_pk == u'3': # pragma: no cover
                phase = "Graduation"
                t_res = Terminated_Resident(resident=resident, resident_first=res_first, resident_last=res_last, date=form.cleaned_data["date"], reason=form.cleaned_data['reason'], phase=phase, race=resident.race)
                t_res.save()
            tr = Termination_Report(resident_first=res_first, resident_last=res_last, date=form.cleaned_data["date"], reason=form.cleaned_data['reason'], phase=phase, race=resident.race)
            tr.save()
            resident.delete()
            resident_data = Resident.objects.all()
            return render(request, 'resident_manage.html', {
                'resident_data' : resident_data
            })
        return render(request, 'resident_home.html')
    else:
        form = TerminationForm(label_suffix="")
        return render(request, 'resident_termination.html', {
            'form': form,
            'resident': resident
        })




def resident_addReport(request, resident_pk):
    """ displays and creates report for residents """
    form = ReportForm(label_suffix="")
    resident = Resident.objects.get(uniqueid=resident_pk)
    if request.method == "POST":
        resident_data = Resident.objects.all()
        form = ReportForm(request.POST, label_suffix="")
        if form.is_valid(): # pragma : no cover
            r = Resident_Report(
			resident = resident,
			activity_type = form.cleaned_data["activity_type"],
			comment = form.cleaned_data["comment"],
			date_added = form.cleaned_data["date_added"]
		)
            r.save()
        return render(request, 'resident_manage.html', {
            'resident_data': resident_data,
        })
    else :
        form = ReportForm(label_suffix="")
        return render(request, 'resident_addReport.html', {
                'form':form,
                'resident':resident,
        })
            

def resident_editReport(request, report_pk):
    """ displays the report form with the passed in report's form values """
    report = Resident_Report.objects.get(uniqueid=report_pk)
    res_report = model_to_dict(report)
    form = ReportForm(request.POST, res_report)
    if request.method == "POST":
        if form.is_valid(): # pragma : no cover
            activity_type = form.cleaned_data["activity_type"]
            comment = form.cleaned_data["comment"]
            report.activity_type = activity_type
            report.comment= comment
            report.save()
            #return render(request, 'resident_home.html')
        resident = report.resident
        reports = Resident_Report.objects.all().filter(resident=resident)
        return render(request, 'resident_report.html', {
            'reports':reports,
            'resident':resident
        })
    else:
        form = ReportForm(res_report)
        return render(request, 'resident_editReport.html', {
            'form': form
        })




def resident_viewReport(request, resident_pk):
    """ Displays the report associated with the passed in report primary key """
    resident = Resident.objects.get(uniqueid=resident_pk)
    reports = Resident_Report.objects.all().filter(resident=resident)
    return render(request, 'resident_report.html', {
        'reports':reports,
        'resident':resident
    })




class demo():
    """ initialiaze statistics values """
    total = 0
    AMAL = 0
    AS = 0
    BL = 0
    HPI = 0
    WH = 0
    HI = 0
    BL_str = 'Black or African American'
    WH_str = 'White'
    AMAL_str =  'American Indian or Alaska Native'
    AS_str = 'Asian'
    HPI_str =  'Native Hawaiian or Other Pacific Islander'
    HI_str = "Hispanic or Latino"
    per_AMAL = 0
    per_AS = 0
    per_BL = 0
    per_HPI = 0
    per_WH = 0
    per_HI = 0

    def __init__(self):
        self.total = 0
        self.AMAL = 0
        self.AS = 0
        self.BL = 0
        self.HPI = 0
        self.WH = 0
        self.HI = 0

    def update_per(self):
        self.per_AMAL = (float(self.AMAL)/float(self.total)) * 100
        self.per_AS = (float(self.AS) / float(self.total)) * 100
        self.per_BL = (float(self.BL) / float(self.total)) * 100
        self.per_HPI = (float(self.HPI) / float(self.total)) * 100
        self.per_WH = (float(self.WH) / float(self.total)) * 100
        self.per_HI = (float(self.HI) / float(self.total)) * 100


    def inc_AMAL(self): # functions to increase race count
        self.AMAL +=1
        self.total +=1
    def inc_AS(self):
        self.AS +=1
        self.total +=1
    def inc_BL(self):
        self.BL +=1
        self.total +=1
    def inc_HPI(self):
        self.HPI +=1
        self.total +=1
    def inc_WH(self):
        self.WH +=1
        self.total +=1
    def inc_HI(self):
        self.HI +=1
        self.total +=1


def resident_demographics(request): # generates statistics on resident demographics
    post_interview = Resident.objects.filter(validated=0)
    pre_interview = Resident_Application.objects.all()
    past_applicants = Termination_Report.objects.all()
    applications = chain(post_interview, pre_interview, past_applicants)
    all_residents = Resident.objects.filter(validated=1)
    dem_res = demo()
    dem_app = demo()
    for res in all_residents: # pragma : no cover
        if res.race == u'Black or African American':
            dem_res.inc_BL()
        elif res.race == u'White':
            dem_res.inc_WH()
        elif res.race == u'American Indian or Alaska Native':
            dem_res.inc_AMAL()
        elif res.race == u'Asian':
            dem_res.inc_AS()
        elif res.race == u'Native Hawaiian or Other Pacific Islander':
            dem_res.inc_HPI()
        elif res.race == u'Hispanic or Latino':
            dem_res.inc_HI()
    if dem_res.total != 0:
        dem_res.update_per()

    for app in applications: # pragma : no cover
        if app.race == u'Black or African American':
            dem_app.inc_BL()
        elif app.race == u'White':
            dem_app.inc_WH()
        elif app.race == u'American Indian or Alaska Native':
            dem_app.inc_AMAL()
        elif app.race == u'Asian':
            dem_app.inc_AS()
        elif app.race == u'Native Hawaiian or Other Pacific Islander':
            dem_app.inc_HPI()
        elif app.race == u'Hispanic or Latino':
            dem_app.inc_HI()
    if dem_app.total != 0:
        dem_app.update_per()
    return render(request, 'resident_demographics.html', {
        'demo_res': dem_res,
        'demo_app': dem_app
    })


class ApplicationWizard(SessionWizardView):
    """ Application wizard to split up the application form into pages"""
    template_name="application_form.html"

    def done(self, form_list, **kwargs): # pragma : no cover
        form_data = process_form_data(form_list)

        return render_to_response('done.html', {'form_data':form_data})

def process_form_data(form_list): # pragma : no cover
    form_data = [form.cleaned_data for form in form_list]

    return form_data
    
