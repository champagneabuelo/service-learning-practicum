"""georgias URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^residents/', include('residents.urls')),
    url(r'^$', views.show_home, name='show_home'),
    url(r'^about/', views.show_about, name='show_about'),
    url(r'^contact/', views.show_contact, name='show_contact'),
    url(r'^donate/', views.show_donate, name='show_donate'),
    url(r'^donate_online/', views.show_donate_page, name='show_donate_page'),
    url(r'^gifts/', views.show_gifts, name='show_gifts'),
    url(r'^volunteer/', views.show_volunteer, name='show_volunteer'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^admin_residents/', views.admin_res, name='admin_res'),
    url(r'^admin_residents_all/', views.admin_res_all, name='admin_res_all'),
    url(r'^admin_residents_curr/', views.admin_res_curr, name='admin_res_curr'),
    url(r'^admin_residents_apps/', views.admin_res_apps, name='admin_res_apps'),
    url(r'^admin_staff/', views.admin_staff, name='admin_staff'),
    url(r'^admin_add_staff/', views.admin_add_staff, name='admin_add_staff'),
    url(r'^admin_donate/', views.admin_donate, name='admin_donate'),
    url(r'^admin_donate_sort_1/', views.admin_donate_sort_1, name='admin_donate_sort_1'),
    url(r'^admin_donate_sort_2/', views.admin_donate_sort_2, name='admin_donate_sort_2'),
    url(r'^admin_donate_sort_3/', views.admin_donate_sort_3, name='admin_donate_sort_3'), 
    url(r'^admin_donation_stats/', views.admin_donation_stats, name='admin_donation_stats'),
    url(r'^delete_donation/(\d+)', views.delete_donation, name='delete_don'),
    url(r'^edit_donation/(\d+)', views.edit_donation, name='edit_don'),
    url(r'^admin_donate_email/', views.admin_donate_email, name='admin_donate_email'),
    url(r'^volunteerHours/', views.create_volunteerHours, name='volunteer_hours'),
    url(r'^delete_hour/(\d+)', views.delete_hour, name='delete_hours'),
    url(r'^admin_profile/', views.admin_profile, name='admin_profile'),
    url(r'^staff_profile/', views.staff_profile, name='staff_profile'),
    url(r'^user_edit_profile/', views.user_edit_profile, name='user_edit_profile'),
    url(r'^contact_mail/', views.contact_mail, name='contact_mail'),
    url(r'^enable_user/(\d+)', views.enable_user, name='enable_user'),
    url(r'^disable_user/(\d+)', views.disable_user, name='disable_user'),
    url(r'^delete_user/(\d+)', views.delete_user, name='delete_user'),
    url(r'^upload_csv/', views.import_csv, name='upload_csv'),
    url(r'^incident_report/', views.incident_report, name='incident_report'),
    url(r'^edit_report/(\d+)', views.admin_edit_report, name='admin_edit_report'),
    url(r'^delete_report/(\d+)', views.admin_delete_report, name='admin_delete_report'),
	url(r'^resident_export/', views.residents_download, name='residents_download'),
	url(r'^incident_report_export/', views.incident_report_download, name='incident_report_download'),
	url(r'^application_export/', views.resident_application_download, name='application_download'),
	url(r'^meeting_export/', views.meeting_download, name='meeting_download'),
    url(r'^community_export/', views.community_download, name='community_download'),
    url(r'^employment_export/', views.employment_download, name='employment_download'),
	url(r'^resident_report_download', views.resident_report_download, name='report_download'),
	url(r'^interview_export/', views.interview_download, name='interview_download'),
]
