from georgias import models
from datetime import datetime as dtdatetime
from django.utils import timezone
from georgias.models import UserProfile, Donors, Incident_Report, VolunteerHours
from georgias.forms import IncidentForm, VolunteerHourForm, EditUserForm, EditUserProfileForm, UserForm, UserProfileForm
from residents.models import Resident, Resident_Application, Meeting_Report, Community_Program, Resident_Employment, Interview_Report, Resident_Report
from georgias.models import *
from georgias.forms import *
from residents.models import *
from django.contrib.auth.models import User
from georgias.forms import *
from django import db
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.contrib.auth import hashers, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from itertools import chain

import datetime
import sys
import re
import codecs
import csv

# Home Page Views

def show_home(request):
	""" Displays landing page. """
	return render(request, 'home.html')

def show_about(request):
	""" Displays About Us page. """	
	return render(request, 'about_us.html')

def show_contact(request):
	""" Displays contact page. """	
	return render(request, 'contact.html')

def contact_mail(request):
	""" Displays contact page. """
	if request.method == 'POST':	##TEST
			subject = request.POST['subject']
			message = request.POST['message']
			from_email = request.POST['from']
			sender_name = request.POST['name']
			thanks = "Thank you for your email!"
			if subject and message and from_email and sender_name:
					try:
						   print('test')# send_mail(sender_name+": "+subject, message, from_email, ['coyanab@gmail.com'])
					except BadHeaderError: # pragma: no cover
							return HttpResponse("Invalid header found")
					return render(request, "contact.html", {'thanks':thanks})
			else:
				   return HttpResponse("Make sure all fields are entered and valid.")  # pragma: no cover       

def show_donate(request):
	""" Display donation page. """		
	return render(request, 'donate.html')

def show_gifts(request):
	""" Show gifts page. """
	return render(request, 'gifts.html')

def show_volunteer(request):
	""" Display volunteer page. """
	return render(request, 'volunteer.html')

def show_donate_page(request):
	""" Display donation page, handle form and form errors. """
	message = ''
	error = False
	if request.method == 'POST':
		donorFirstName = request.POST['donorFirstName']
		donorLastName = request.POST['donorLastName']
		donationAmount = request.POST['donationAmount']
		donorEmail = request.POST['donorEmail']
		if donorFirstName and donorLastName and donationAmount and donorEmail:
			if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", donorEmail) is not None:
				newDonor = Donors()
				newDonor.donorFirstName = donorFirstName
				newDonor.donorLastName = donorLastName
				if re.match(r'\d', donorFirstName) is None and re.match(r'\d', donorLastName) is None:
					try:
						int(donationAmount)
					except:
						error = True
						message = "Please enter donation amount as a whole number"
						return render(request, 'donate_page.html', {'error': error, 'message': message})
					newDonor.donationAmount = donationAmount
					newDonor.donorEmail = donorEmail
					newDonor.donationDate = datetime.date.today()
					try:  
						newDonor.save()
					except: # pragma: no cover
						error = True
						message = "System error!"
						return render(request, 'donate_page.html', {'error': error, 'message': message})
					return HttpResponseRedirect("https://www.gofundme.com/ghh-cville")
				else:
					error = True
					message = "Please enter a valid name."
					return render(request, 'donate_page.html', {'error': error, 'message': message})
			else:
				error = True
				message = "Please enter a valid email!"
				return render(request, 'donate_page.html', {'error': error, 'message': message})
		else:
			error = True
			message = "Make sure all fields are entered and valid."
			return render(request, 'donate_page.html', {'error': error, 'message':message})
	else:
		return render(request, 'donate_page.html', {'error': error, 'message': message})

# User Login Views

def user_login(request): # pragma: no cover
	if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)

			if user:
					if user.is_active: ##TEST
							login(request, user)
							curr_user = UserProfile.objects.get(user_id = user.id)
							user_type = curr_user.user_type
							if user_type == 'ADM':
									return redirect(admin_profile)
							else:
									return redirect(staff_profile)
					else:
							return HttpResponse("Your account is disabled")
			else:
					print("User not authenticated")
					return render(request, "login.html")
	return render(request, "login.html")


def user_logout(request): # pragma: no cover
	logout(request)	##TEST
	return render(request, "home.html")

# Volunteer Hour Views

def create_volunteerHours(request): # pragma: no cover
	""" 
	Displays the VolunteerHourForm form to the user, and saves the data if the form is valid. 
		If the user is authenticated (i.e. is a admin or staff):
			display volunteer form with initial info filled in. 
		Else: 
			display blank voluteer form.	
	"""
	if request.method == 'POST':
		hours_form = VolunteerHourForm(data=request.POST, 	##TEST
						initial={"volDate": datetime.date.today()})
		if hours_form.is_valid():
			hours = hours_form.save()
			hours.save()
		else:
			print(hours_form.errors)

	else:
		if request.user.is_anonymous:
			hours_form = VolunteerHourForm()	##TEST
		else:
			hours_form = VolunteerHourForm(initial={'volunteer': request.user})
		#hours_form.save()
	if request.user.is_authenticated():
		volHours = VolunteerHours.objects.all().filter(volunteer=request.user)
	else:
		volHours = VolunteerHours.objects.all()   ##TEST
	return render(request, 'subVolHours.html', {'hours_form' : hours_form, 'volHours' : volHours})

@login_required()
def delete_hour(request, volunteer_id):
	""" Deletes an instance of volunteer hours. """
	try:
		h = VolunteerHours.objects.get(pk=volunteer_id)
	except ObjectDoesNotExist:
		#print('HELP1')
		return redirect('/volunteerHours/')
	h.delete()
	return redirect('/volunteerHours/')

# Admin Operation Views

@login_required()
def enable_user(request, user_id):
	""" Enables a disabled user. """
	try:	##TEST
		u = UserProfile.objects.get(pk=user_id)
	except UserProfile.DoesNotExist:
		return redirect(reverse('admin_staff'))
	u.user.is_active = True
	u.user.save()
	return redirect(reverse('admin_staff'))

@login_required()
def disable_user(request, user_id):
	""" Disables an active user. """
	try:	##TEST
		u = UserProfile.objects.get(pk=user_id)
	except UserProfile.DoesNotExist:
		return redirect(reverse('admin_staff'))
	u.user.is_active = False
	u.user.save()
	return redirect(reverse('admin_staff'))

@login_required()
def delete_user(request, user_id):
	""" Removes a user (staff or admin) from the system. """	
	admin = request.user.is_superuser	##TEST
	if admin:
		try:
				u = UserProfile.objects.get(pk=user_id)
		except UserProfile.DoesNotExist:
				return redirect('/admin_staff/')
		u.delete()
		return redirect('/admin_staff/')
	else: # pragma: no cover
		return redirect('/admin_staff/')

@login_required()
def delete_donation(request, don_id): #pragma: no cover
	""" Removes a donation record from the system. """
	error_message = ''
	try:
		d = Donors.objects.get(pk=don_id)
	except ObjectDoesNotExist:
		error_message = "Failed to delete donation."
		return render(request, 'admin_donate.html', {'error_message': error_message})
        d.delete()
        return redirect(reverse('admin_donate'))
	#return render(request, 'admin_donate.html', {'error_message': error_message})

@login_required()		
def edit_donation(request, don_id): # pragma: no cover
	""" Edit the information associated with a donation record. """
	try:
		d = Donors.objects.get(pk=don_id)
	except ObjectDoesNotExist:
		return redirect('/admin_donate/')
	message = ''
        error = False
        if request.method == 'POST':
                donorFirstName = request.POST['donorFirstName']
                donorLastName = request.POST['donorLastName']
                donationAmount = request.POST['donationAmount']
                donorEmail = request.POST['donorEmail']
		#donationDate = request.POST['donationDate']
                if donorFirstName and donorLastName and donationAmount and donorEmail:
                        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", donorEmail) is not None:
                                d.donorFirstName = donorFirstName
                                d.donorLastName = donorLastName
                                if re.match(r'\d', donorFirstName) is None and re.match(r'\d', donorLastName) is None:
                                        try:
                                                int(donationAmount)
                                        except:
                                                error = True
                                                message = "Please enter donation amount as a whole number"
                                                return render(request, 'edit_donation.html', {'Donor': d, 'error': error, 'message': message})
                                        d.donationAmount = donationAmount
                                        d.donorEmail = donorEmail
                                       #d.donationDate = parse_date(donationDate)
                                        try:
						d.save()
                                        except:
                                                error = True
                                                message = "System error!"
                                                return render(request, 'edit_donation.html', {'Donor': d, 'error': error, 'message': message})
                                        return redirect(reverse('admin_donate'))
					#donors = Donors.objects.all()
                                        #return render(request, 'admin_donate.html', {'donors' : donors,'error': error, 'message': message})
                                else:
                                        error = True
                                        message = "Please enter a valid name!"
                                        return render(request, 'edit_donation.html', {'Donor': d, 'error': error, 'message': message})

                        else:
                                error = True
                                message = "Please enter a valid email!"
                                return render(request, 'edit_donation.html', {'Donor': d, 'error': error, 'message': message})
                else:
                        error = True
                        message = "Make sure all fields are entered and valid."
                        return render(request, 'edit_donation.html', {'Donor' : d, 'error': error, 'message':message})
        else:
           return render(request, 'edit_donation.html', {'Donor': d, 'error': error, 'message': message})
   
@login_required()
def admin_delete_report(request, report_id): 
	""" Delete a critical incident report. """
	user = request.user
	if user:
            try:
                report = Incident_Report.objects.get(pk=report_id)
            except ObjectDoesNotExist:
		return redirect(reverse('incident_report'))
            report.delete()
            return redirect(reverse('incident_report'))
        else: # pragma: no cover
            return redirect(reverse('incident_report')) 
   
@login_required() 
def admin_edit_report(request, report_id):
	""" Edit the contents of a critical incident report. """
	user = request.user
	if user:
		try: 
			report = Incident_Report.objects.get(pk=report_id)
		except ObjectDoesNotExist:
			return redirect(reverse('incident_report'))
		if request.method == "GET":
			try:
				form = IncidentForm(instance=report)
  				return render(request, 'edit_incident_report.html', {'form': form})
			except ObjectDoesNotExist: # pragma: no cover
				return redirect(reverse('incident_report'))
		elif request.method == "POST":	##TEST
			form = IncidentForm(request.POST, instance=report)
			if form.is_valid():
				incident = form.save(commit=False)
				#form.involved = form.cleaned_data.get('involved')
				#print(form)
				incident.save()
				form.save_m2m()
				form = IncidentForm()
			return redirect(reverse('incident_report'))
	else: # pragma: no cover
		return redirect(reverse('incident_report'))

@login_required()
def admin_donate_email(request): # pragma: no cover
	""" Send an email to all donors. """
	emails = Donors.objects.values_list('donorEmail', flat=True)
	error = ''
	success = True
	if request.method == 'POST':
                subject = request.POST['subject']
                message = request.POST['message']
		sender_name = "Georgia's Healing House"
		#emails = Donors.objects.values_list('donorEmail', flat=True)[0]
                for email in emails:
                	if subject and message:
                        	try:
                	               	send_mail(sender_name+": "+subject, message, 'coyanab@gmail.com', [email], fail_silently=False)
                     		except BadHeaderError:
					error = "Invalid header found"
					success = False
                                	return render(request, "admin_donate_email.html", {'error':error, 'success':success})
                	else:
				error = "Make sure all fields are entered and valid."
				success = False
                      		return render(request, "admin_donate_email.html", {'error':error, 'success':success})
		return render(request, 'admin_donate_email.html', {'error': error, 'success':success})
	else:
		return render(request, 'admin_donate_email.html', {'error': error, 'success':False})

@login_required()
def admin_donation_stats(request): # pragma: no cover
	""" Get information based on donation statistics. """ 
	donors = Donors.objects.all()
	count = 0
	sum = 0
	average = 0
	for d in donors:
		count += 1
		sum += d.donationAmount
        if count != 0:
            average = sum/count
	return render(request, 'admin_donation_stats.html', {'average': average, 'count': count, 'total': sum})

@login_required()
def admin_res(request):
	return render(request, 'admin_residents.html')

@login_required()
def admin_res_all(request):
	return render(request, 'admin_residents_all.html')#, {'all':res_all})

@login_required()
def admin_res_curr(request):
	residents = Resident.objects.all()
	return render(request, 'admin_residents_curr.html', {'residents':residents})

@login_required()
def admin_res_apps(request):
	applicants = Resident_Application.objects.all()
	return render(request, 'admin_residents_apps.html', {'applicants':applicants})

@login_required
@user_passes_test(lambda u: UserProfile.objects.get(user=u).user_type == 'ADM', login_url='/admin_profile/')

def admin_staff(request):
	staff = UserProfile.objects.all().filter(user_type="STF")
        return render(request, 'admin_staff.html', {'staff_list':staff})

#@login_required()
def admin_add_staff(request):
	""" Create a new admin or staff member. """
	registered = False
	registration_message = ''
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)	##TEST
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.password = hashers.make_password(user.password)
			user.save()	
			profile = profile_form.save(commit = False)
			profile.user = user
			profile.save()
			registered = True
			registration_message = "You have created a staff member successfully!"
		else:
			registration_message = "You were unable to create a new staff member. Please try again"
	else:	
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'admin_add_staff.html', {'user_form':user_form,
											 'profile_form':profile_form,
											 'registered':registered,
											 'reg_message':registration_message})

@login_required() 
def user_edit_profile(request):
	""" Edit the user profile. """	
	user = request.user	##TEST
	current_user = UserProfile.objects.get(user=user)
	if request.method == 'POST':
		user_form = EditUserForm(request.POST, instance=user)
		profile_form = EditUserProfileForm(request.POST, instance=current_user)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()	
			user.save()
			
			profile = profile_form.save(commit = False)
			profile.user = user
			profile.save()
			#if current_user.user_type == 'ADM':
			return HttpResponseRedirect(reverse('admin_profile'))
			#if current_user.user_type == 'STF': 
			#	return HttpResponseRedirect('/admin_profile/')
			
	else:
		admin_dict = model_to_dict(current_user)
		user_dict = model_to_dict(user)
		user_form = EditUserForm(user_dict)
		profile_form = EditUserProfileForm(admin_dict)
	return render(request, 'user_edit_profile.html', {'user_form':user_form,
						 		'current_user':user,
                                                 		'profile_form':profile_form})	

@login_required()	
def admin_donate(request): # pragma: no cover
	donors = Donors.objects.all()
	message = ''
        error = False
        if request.method == 'POST':
                donorFirstName = request.POST['donorFirstName']
                donorLastName = request.POST['donorLastName']
                donationAmount = request.POST['donationAmount']
                donorEmail = request.POST['donorEmail']
                if donorFirstName and donorLastName and donationAmount and donorEmail:
                        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", donorEmail) is not None:
                                newDonor = Donors()
                                newDonor.donorFirstName = donorFirstName
                                newDonor.donorLastName = donorLastName
                                if re.match(r'\d', donorFirstName) is None and re.match(r'\d', donorLastName) is None:
                                        try:
                                                int(donationAmount)
                                        except:
                                                error = True
                                                message = "Please enter donation amount as a whole number"
                                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                                        newDonor.donationAmount = donationAmount
                                        newDonor.donorEmail = donorEmail
                                        newDonor.donationDate = datetime.date.today()
                                        try:
                                                newDonor.save()
                                        except:
                                                error = True
                                                message = "System error!"
                                                return render(request, 'admin_donate.html', {'error': error, 'message': message})
                                       	return render(request, 'admin_donate.html', {'donors' : donors,'error': error, 'message': message})
				else:
                                        error = True
                                        message = "Please enter a valid name."
                                        return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

                        else:
                                error = True
                                message = "Please enter a valid email!"
                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                else:
                        error = True
                        message = "Make sure all fields are entered and valid."
                        return render(request, 'admin_donate.html', {'donor' : donors, 'error': error, 'message':message})
        else:
           return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})



def admin_donate_sort_1(request): # pragma: no cover
	""" Sorting donation by date. """ 
	donors = Donors.objects.all().order_by('-donationDate')
	message = ''
        error = False
        if request.method == 'POST':
                donorFirstName = request.POST['donorFirstName']
                donorLastName = request.POST['donorLastName']
                donationAmount = request.POST['donationAmount']
                donorEmail = request.POST['donorEmail']
                if donorFirstName and donorLastName and donationAmount and donorEmail:
                        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", donorEmail) is not None:
                                newDonor = Donors()
                                newDonor.donorFirstName = donorFirstName
                                newDonor.donorLastName = donorLastName
                                if re.match(r'\d', donorFirstName) is None and re.match(r'\d', donorLastName) is None:
                                        try:
                                                int(donationAmount)
                                        except:
                                                error = True
                                                message = "Please enter donation amount as a whole number"
                                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                                        newDonor.donationAmount = donationAmount
                                        newDonor.donorEmail = donorEmail
                                        newDonor.donationDate = datetime.date.today()
                                        try:
                                                newDonor.save()
                                        except:
                                                error = True
                                                message = "System error!"
                                                return render(request, 'admin_donate.html', {'error': error, 'message': message})
                                       	return render(request, 'admin_donate.html', {'donors' : donors,'error': error, 'message': message})
				else:
                                        error = True
                                        message = "Please enter a valid name."
                                        return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

                        else:
                                error = True
                                message = "Please enter a valid email!"
                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                else:
                        error = True
                        message = "Make sure all fields are entered and valid."
                        return render(request, 'admin_donate.html', {'donor' : donors, 'error': error, 'message':message})
        else:
           return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

def admin_donate_sort_2(request): # pragma: no cover
	""" Sorting donations be amount (largest to smallest) """
	donors = Donors.objects.all().order_by('donationAmount')
	message = ''
        error = False
        if request.method == 'POST':
                donorFirstName = request.POST['donorFirstName']
                donorLastName = request.POST['donorLastName']
                donationAmount = request.POST['donationAmount']
                donorEmail = request.POST['donorEmail']
                if donorFirstName and donorLastName and donationAmount and donorEmail:
                        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", donorEmail) is not None:
                                newDonor = Donors()
                                newDonor.donorFirstName = donorFirstName
                                newDonor.donorLastName = donorLastName
                                if re.match(r'\d', donorFirstName) is None and re.match(r'\d', donorLastName) is None:
                                        try:
                                                int(donationAmount)
                                        except:
                                                error = True
                                                message = "Please enter donation amount as a whole number"
                                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                                        newDonor.donationAmount = donationAmount
                                        newDonor.donorEmail = donorEmail
                                        newDonor.donationDate = datetime.date.today()
                                        try:
                                                newDonor.save()
                                        except:
                                                error = True
                                                message = "System error!"
                                                return render(request, 'admin_donate.html', {'error': error, 'message': message})
                                       	return render(request, 'admin_donate.html', {'donors' : donors,'error': error, 'message': message})
				else:
                                        error = True
                                        message = "Please enter a valid name."
                                        return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

                        else:
                                error = True
                                message = "Please enter a valid email!"
                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                else:
                        error = True
                        message = "Make sure all fields are entered and valid."
                        return render(request, 'admin_donate.html', {'donor' : donors, 'error': error, 'message':message})
        else:
           return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

def admin_donate_sort_3(request): # pragma: no cover
	"""Sorting donations by amount (smallest to largest) """ 
	donors = Donors.objects.all().order_by('-donationAmount')
	message = ''
        error = False
        if request.method == 'POST':
                donorFirstName = request.POST['donorFirstName']
                donorLastName = request.POST['donorLastName']
                donationAmount = request.POST['donationAmount']
                donorEmail = request.POST['donorEmail']
                if donorFirstName and donorLastName and donationAmount and donorEmail:
                        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", donorEmail) is not None:
                                newDonor = Donors()
                                newDonor.donorFirstName = donorFirstName
                                newDonor.donorLastName = donorLastName
                                if re.match(r'\d', donorFirstName) is None and re.match(r'\d', donorLastName) is None:
                                        try:
                                                int(donationAmount)
                                        except:
                                                error = True
                                                message = "Please enter donation amount as a whole number"
                                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                                        newDonor.donationAmount = donationAmount
                                        newDonor.donorEmail = donorEmail
                                        newDonor.donationDate = datetime.date.today()
                                        try:
                                                newDonor.save()
                                        except:
                                                error = True
                                                message = "System error!"
                                                return render(request, 'admin_donate.html', {'error': error, 'message': message})
                                       	return render(request, 'admin_donate.html', {'donors' : donors,'error': error, 'message': message})
				else:
                                        error = True
                                        message = "Please enter a valid name."
                                        return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

                        else:
                                error = True
                                message = "Please enter a valid email!"
                                return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})
                else:
                        error = True
                        message = "Make sure all fields are entered and valid."
                        return render(request, 'admin_donate.html', {'donor' : donors, 'error': error, 'message':message})
        else:
           return render(request, 'admin_donate.html', {'donors': donors, 'error': error, 'message': message})

# CSV export functionality
## Resident
def export_residents(request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="residentdata.csv"'
	writer = csv.writer(response)
	writer.writerow([
		smart_str(u"Resident ID"),
		smart_str(u"Interview Report ID"),
		smart_str(u"First Name"),
		smart_str(u"Last Name"),
		smart_str(u"Race"),
		smart_str(u"Date of Birth"),
		smart_str(u"Join Date"),		
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.uniqueid),
			smart_str(obj.interview_report),
			smart_str(obj.resident_first),
			smart_str(obj.resident_last),
			smart_str(obj.race),
			smart_str(obj.date_of_birth),
			smart_str(obj.join_date),
		])
	return response

def residents_download(request):
	data = export_residents(request, Resident.objects.all())
	return data

## Resident Applications
def export_resident_applications(request, queryset): # pragma: no cover
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="applicationdata.csv"'
	writer = csv.writer(response)
	writer.writerow([
		smart_str(u"Application ID"),
		smart_str(u"Interview Report ID"),
		smart_str(u"First Name"),
		smart_str(u"Last Name"),
		smart_str(u"Date of Birth"),
		smart_str(u"Race"),
		smart_str(u"Email"),
		smart_str(u"Phone Number"),
		smart_str(u"Mailing Address"),
		smart_str(u"Physical Address"),
		smart_str(u"Time at Physical Address"),
		smart_str(u"Level of Education"),
		smart_str(u"Has Children"),
		smart_str(u"Has Custody"),
		smart_str(u"Married/Relationship"),
		smart_str(u"Spouse Name"),
		smart_str(u"Spouse Age"),
		smart_str(u"Receiving Income"),
		smart_str(u"Drivers License"),
		smart_str(u"Alcohol Use"),
		smart_str(u"Drug Use"),
		smart_str(u"Phone Number"),
		smart_str(u"Currently Sober"),
		smart_str(u"Length of Sobriety"),
		smart_str(u"Attending AA/NA"),
		smart_str(u"AA or NA"),
		smart_str(u"Currently in AA/NA"),
		smart_str(u"Last AA/NA Meeting"),
		smart_str(u"Currently smokes"),
		smart_str(u"Willing to quit"),
		smart_str(u"Has been homeless"),
		smart_str(u"Has attempted suicide"),
		smart_str(u"Has experience domestic violence"),
		smart_str(u"Has been incarcerated"),
		smart_str(u"Number of incarcerations"),
		smart_str(u"Currently incarcerated"),
		smart_str(u"On probation"),
		smart_str(u"What can GHH provide"),
		smart_str(u"Benefits from residency"),
		smart_str(u"Goals in months"),
		smart_str(u"Obstacles for Goals"),
		smart_str(u"Applicant attributes"),
		smart_str(u"Applicant essay"),
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.uniqueid),
			smart_str(obj.interview_report),
			smart_str(obj.resident_first),
			smart_str(obj.resident_last),
			smart_str(obj.date_of_birth),
			smart_str(obj.race),
			smart_str(obj.email),
			smart_str(obj.phone_number),
			smart_str(obj.mailing_address),
			smart_str(obj.physical_address),
			smart_str(obj.length_at_phys_addr),
			smart_str(obj.level_of_education),
			smart_str(obj.has_children),
			smart_str(obj.has_custody),
			smart_str(obj.is_married_or_relationship),
			smart_str(obj.spouse_name),
			smart_str(obj.spouse_age),
			smart_str(obj.is_receiving_income),
			smart_str(obj.has_va_license),
			smart_str(obj.uses_alcohol),
			smart_str(obj.uses_drugs),
			smart_str(obj.currently_sober),
			smart_str(obj.length_of_sobriety),
			smart_str(obj.ever_been_to_aa_na),
			smart_str(obj.aa_or_na),
			smart_str(obj.currently_in_aa_na),
			smart_str(obj.last_aa_na_meeting),
			smart_str(obj.currently_smokes),
			smart_str(obj.willing_to_quit),
			smart_str(obj.has_been_homeless),
			smart_str(obj.has_attempted_suicide),
			smart_str(obj.has_experienced_dom_violence),
			smart_str(obj.has_been_incarcerated),
			smart_str(obj.number_of_incar),
			smart_str(obj.currently_incar),
			smart_str(obj.on_probation),
			smart_str(obj.what_ghh_can_provide),
			smart_str(obj.benefits_from_residency),
			smart_str(obj.goals_in_months),
			smart_str(obj.obstacles_for_goals),
			smart_str(obj.applicant_attributes),
			smart_str(obj.applicant_essay),
		])
	return response

def resident_application_download(request): # pragma: no cover
	data = export_resident_applications(request, Resident_Application.objects.all())
	return data


## Interview Reports
def export_interview_reports(request, queryset): # pragma: no cover
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=interviewdata.csv'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))

	writer.writerow([
		smart_str(u"First Name"),
		smart_str(u"Last Name"),
		smart_str(u"Last permanent address"),
		smart_str(u"Emergency Contact Name"),
		smart_str(u"Emergency Contact Relationship"),
		smart_str(u"Phone number"),
		smart_str(u"Significant Other Name"),
		smart_str(u"Significant Other Relationship"),
		smart_str(u"Custody of Children"),
		smart_str(u"Source of Income"),
		smart_str(u"Job History"),
		smart_str(u"Job Skills"),
		smart_str(u"Valid Drivers License"),
		smart_str(u"Recent Arrests"),
		smart_str(u"Alcohol history"),
		smart_str(u"Prescription history"),
		smart_str(u"Opiates history"),
		smart_str(u"Cocaine history"),
		smart_str(u"Marijuana history"),
		smart_str(u"Others history"),
		smart_str(u"Legal consequences"),
		smart_str(u"Health consequences"),
		smart_str(u"Family, social consequences"),
		smart_str(u"Work consequences"),
		smart_str(u"Substance abuse treatment"),
		smart_str(u"Other Substance Abuse notes"),
		smart_str(u"Physical abuse history"),
		smart_str(u"Physical abuse comment"),
		smart_str(u"Emotional abuse history"),
		smart_str(u"Emotional abuse comment"),
		smart_str(u"Physicians and location"),
		smart_str(u"Medical problem"),
		smart_str(u"Current Medications"),
		smart_str(u"Agencies involved"),
		smart_str(u"Reference Name"),
		smart_str(u"Reference relationship"),
		smart_str(u"Reference phone number"),
		smart_str(u"Level of education"),
		smart_str(u"Interest in further"),
		smart_str(u"Interest, skills, hobbies"),
		smart_str(u"For fun"),
		smart_str(u"Specific goals"),
		smart_str(u"Comment"),
	])
	for res in queryset:
		obj = res.interview_report
		writer.writerow([
			smart_str(res.resident_first),
			smart_str(res.resident_last),
			smart_str(obj.last_perm_address),
			smart_str(obj.emergency_contact_name),
			smart_str(obj.emergency_contact_relationship),
			smart_str(obj.phone_number),
			smart_str(obj.significant_other_name),
			smart_str(obj.significant_other_relationship),
			smart_str(obj.custody_of_children),
			smart_str(obj.source_of_income),
			smart_str(obj.job_history),
			smart_str(obj.job_skills),
			smart_str(obj.valid_drivers_license),
			smart_str(obj.recent_arrests),
			smart_str(obj.alcohol_history),
			smart_str(obj.prescription_history),
			smart_str(obj.opiates_history),
			smart_str(obj.cocaine_history),
			smart_str(obj.marijuana_history),
			smart_str(obj.others_history),
			smart_str(obj.legal_consequences),
			smart_str(obj.health_consequences),
			smart_str(obj.family_social_consequences),
			smart_str(obj.work_consequences),
			smart_str(obj.sa_treatment),
			smart_str(obj.sa_other_notes),
			smart_str(obj.physical_abuse_history),
			smart_str(obj.physical_abuse_comment),
			smart_str(obj.emotional_abuse_history),
			smart_str(obj.emotional_abuse_comment),
			smart_str(obj.physicians_and_location),
			smart_str(obj.medical_problems),
			smart_str(obj.current_medications),
			smart_str(obj.agencies_involved),
			smart_str(obj.reference_name),
			smart_str(obj.reference_relationship),
			smart_str(obj.reference_phone),
			smart_str(obj.level_of_education),
			smart_str(obj.interest_in_further),
			smart_str(obj.interest_skills_hobbies),
			smart_str(obj.for_fun),
			smart_str(obj.specific_goals),
			smart_str(obj.comment),

		])
	return response

def interview_download(request): # pragma: no cover
	data = export_interview_reports(request, Resident.objects.filter(validated=0))
	return data



## Incident Reports
def export_incident_reports(request, queryset): # pragma: no cover
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=incidentdata.csv'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))
	writer.writerow([
		smart_str(u"Report ID"),
		smart_str(u"Staff ID"),
		smart_str(u"Resident ID"),
		smart_str(u"Incident Type"),
		smart_str(u"Incident Date"),
		smart_str(u"Date Created"),
		smart_str(u"Comment"),		
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.uniqueid),
			smart_str(obj.staff),
			smart_str(obj.residents),
			smart_str(obj.incident_type),
			smart_str(obj.incident_date),
			smart_str(obj.date_created),
			smart_str(obj.comment),
		])
	return response

def incident_report_download(request): # pragma: no cover
	data = export_incident_reports(request, Incident_Report.objects.all())
	return data



## Meeting Reports
def export_meeting_reports(request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=meetingdata.csv'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))
	writer.writerow([
		smart_str(u"Meeting ID"),
		smart_str(u"Resident ID"),
		smart_str(u"First Name"),
		smart_str(u"Last Name"),
		smart_str(u"Meeting Type"),
		smart_str(u"Meeting Date"),
		smart_str(u"Comment"),		
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.uniqueid),
			smart_str(obj.resident),
			smart_str(obj.resident.resident_first),
			smart_str(obj.resident.resident_last),
			smart_str(obj.meeting_type),
			smart_str(obj.meeting_date),
			smart_str(obj.comment),
		])
	return response

def meeting_download(request):
	data = export_meeting_reports(request, Meeting_Report.objects.all())
	return data


## Community Reports
def export_community_reports(request, queryset): # pragma: no cover
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="communitydata.csv"'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))
	writer.writerow([
		smart_str(u"First Name"),
		smart_str(u"Last Name"),
		smart_str(u"Program Name"),
		smart_str(u"Description"),
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.resident.resident_first),
			smart_str(obj.resident.resident_last),
			smart_str(obj.program_name),
			smart_str(obj.description),
		])
	return response


def community_download(request):# pragma: no cover
	data = export_community_reports(request, Community_Program.objects.all())
	return data	


## Employment Reports
def export_employment_reports(request, queryset): # pragma: no cover
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="employmentdata.csv"'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))
	writer.writerow([
		smart_str(u"First Name"),
		smart_str(u"Last Name"),
		smart_str(u"Employer"),
		smart_str(u"Position"),
		smart_str(u"Start Date"),
		smart_str(u"End Date"),
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.resident.resident_first),
			smart_str(obj.resident.resident_last),
			smart_str(obj.employer),
			smart_str(obj.position),
			smart_str(obj.start_date),
			smart_str(obj.end_date),
		])
	return response

def employment_download(request):# pragma: no cover
	data = export_employment_reports(request, Resident_Employment.objects.all())
	return data	


## Resident Reports
def export_resident_reports(request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=reportdata.csv'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))
	writer.writerow([
		smart_str(u"Report ID"),
		smart_str(u"Resident ID"),
		smart_str(u'First Name'),
		smart_str(u'Last Name'),
		smart_str(u"Report Type"),
		smart_str(u"Date Added"),
		smart_str(u"Comment"),		
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.uniqueid),
			smart_str(obj.resident),
			smart_str(obj.resident.resident_first),
			smart_str(obj.resident.resident_last),
			smart_str(obj.activity_type),
			smart_str(obj.date_added),
			smart_str(obj.comment),
		])
	return response

def resident_report_download(request):
	data = export_resident_reports(request, Resident_Report.objects.all())
	return data

## Termination Reports
def export_termination_reports(request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=reportdata.csv'
	writer = csv.writer(response, csv.excel)
	response.write(''.encode('utf8'))
	writer.writerow([
		smart_str(u"Report ID"),
		smart_str(u"Resident ID"),
		smart_str(u"Report Type"),
		smart_str(u"Date Added"),
		smart_str(u"Comment"),		
	])
	for obj in queryset:
		writer.writerow([
			smart_str(obj.uniqueid),
			smart_str(obj.resident),
			smart_str(obj.activity_type),
			smart_str(obj.date_added),
			smart_str(obj.comment),
		])
	return response

def resident_report_download(request):
	data = export_resident_reports(request, Resident_Report.objects.all())
	return data





@login_required()
def admin_profile(request):
	""" Display the profile page for admins. """
	user = request.user
	first_name = user.first_name
	last_name = user.last_name
	email = user.email
	username = user.username
	user_profile =  UserProfile.objects.get(user_id = user.id)
	addr = user_profile.user_addr
	homeph = user_profile.user_homeph
	workph = user_profile.user_workph
	return render(request, 'admin_profile.html', {'first_name':first_name, 'last_name':last_name,
												 'email':email, 'username':username, 'addr':addr,
												 'homeph':homeph, 'workph':workph})

# Staff Profile Views

@login_required()
def staff_profile(request):
	""" Display the profile page for staff. """
	user = request.user
	first_name = user.first_name
	last_name = user.last_name
	email = user.email
	username = user.username
	user_profile =  UserProfile.objects.get(user_id = user.id)
	addr = user_profile.user_addr
	homeph = user_profile.user_homeph
	workph = user_profile.user_workph
	return render(request, 'staff_profile.html', {'first_name':first_name, 'last_name':last_name,
												 'email':email, 'username':username, 'addr':addr,
												 'homeph':homeph, 'workph':workph})
@login_required()
def staff_home(request): # pragma: no cover
        return render(request, 'staff_home.html')

# Reporting Views

def import_csv(request): # pragma: no cover
	if request.POST and request.FILES:
		csvfile = request.FILES['csv_file']
		dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
		csvfile.open()
		reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=',', dialect=dialect)
		for row in reader:
			#created = Model.objects.get_or_create(
			#MODEL FIELDS, FIRST ROW WILL BE TYPE OF THING
			#)
			print("placeholder")
		return render(request, "home.html")
	else:
		return render(request, "csv_upload.html")


@login_required() 
def incident_report(request):
	if request.method == 'POST':
		data = request.POST.copy()
		datetime = data['incident_date_0_month'] + '/' + data['incident_date_0_day'] + '/' + data['incident_date_0_year'] + ' ' + data['incident_date_1_hour'] + ':' + data['incident_date_1_minute'] + ':' + data['incident_date_1_second']
		data['incident_date'] = datetime
		del data['incident_date_0_month']
		del data['incident_date_0_day']
		del data['incident_date_0_year']
		del data['incident_date_1_hour']
		del data['incident_date_1_minute']
		del data['incident_date_1_second']
	#	print(data)
		form = IncidentForm(request.POST)
		#print(request.POST.get('incident_date_0_day'))
		if form.is_valid():
			incident = form.save(commit=False)
			#form.involved = form.cleaned_data.get('involved')
		#	print(form)
			incident.save()
			form.save_m2m()
			form = IncidentForm()
	else:
		form = IncidentForm()

	return render(request, "incident_report.html", {'reports': Incident_Report.objects.all(), 'form':form})
