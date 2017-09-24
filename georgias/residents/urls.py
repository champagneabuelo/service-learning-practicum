""" residents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from .models import Resident
from residents.forms import ApplicationForm1, ApplicationForm2, ApplicationForm3
from residents.views import resident_interviewForm, ApplicationWizard

urlpatterns = [
    url(r'^$', views.index, name='resident_home'),
    url(r'^create/$', views.resident_add, name='resident_create'),
    url(r'^manage/$', views.resident_manage, name='resident_manage'),
    url(r'^edit_resident/(?P<resident_pk>.*)$', views.edit_resident, name='edit_resident'),
    url(r'^add_report/(?P<resident_pk>.*)$', views.resident_addReport, name='resident_addReport'),
    url(r'^edit_report/(?P<report_pk>.*)$', views.resident_editReport, name='resident_editReport'),
    url(r'^view_report/(?P<resident_pk>.*)$', views.resident_viewReport, name='resident_viewReport'),
    url(r'^view_application/(?P<resident_pk>.*)$', views.resident_viewApplication, name='resident_viewApplication'),
    url(r'^termination/(?P<resident_pk>.*)/(?P<phase_pk>.*)$', views.resident_termination, name='resident_termination'),
    url(r'^applications/$', views.resident_applications, name='applications'),
    url(r'^demographics/$', views.resident_demographics, name='demographics'),
    url(r'^interview_form/(?P<resident_pk>.*)$', views.wrapped_interview_form , name='interview_form'),
    url(r'^manage_termination/$', views.resident_manage_termination, name='manage_termination'),
    url(r'^apply/$', ApplicationWizard.as_view([ApplicationForm1, ApplicationForm2, ApplicationForm3]), name='apply'),
    url(r'^interview_manage/$', views.resident_manage_interview, name='interview_manage'),
    url(r'^interview_manage/(?P<resident_pk>.*)$', views.resident_viewInterview, name='interview_view'),
    url(r'^reports/', views.resident_reports, name='resident_reports'),
    url(r'^view_reports/(?P<resident_pk>.*)$', views.resident_viewReports, name='reports_view'),
    url(r'^add_meeting/(?P<resident_pk>.*)$', views.resident_addMeeting, name='resident_addMeeting'),
    url(r'^add_program/(?P<resident_pk>.*)$', views.resident_addProgram, name='resident_addProgram'),
    url(r'^add_employment/(?P<resident_pk>.*)$', views.resident_addEmployment, name='resident_addEmployment'),
    url(r'^view_monthlyReports/(?P<resident_pk>.*)$', views.resident_viewMonthlyReports, name='resident_monthlyReports'),
    url(r'^reports_view_interview/(?P<resident_pk>.*)$', views.resident_reportsViewInterview, name='resident_reportsViewInterview'),
    url(r'^reports_view_application/(?P<resident_pk>.*)$', views.resident_reportsViewApplication, name='resident_reportsViewApplication'),        
]
