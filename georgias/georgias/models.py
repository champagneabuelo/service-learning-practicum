import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid

from residents.models import Resident

class UserProfile(models.Model):
	""" Model that stores user login information, permissions, user data. """
	ADMIN = 'ADM'
	STAFF = 'STF' 
	USER_TYPE_CHOICES = ((ADMIN, 'Admin'), (STAFF, 'Staff'),)
	user = models.OneToOneField(User, related_name='user')	
        user_type = models.CharField(max_length = 30, 
					choices = USER_TYPE_CHOICES, 
					default = None, 
					null=True)
        user_addr = models.CharField(max_length=300, blank=True)
        user_homeph = models.CharField(max_length = 10, blank=True)
        user_workph = models.CharField(max_length = 10, blank=True)

        def __unicode__(self):
                return self.user.username


class VolunteerHours(models.Model):
	""" Stores information relevant to logging volunteer hours.
		- was_submitted_recently: checks volunteer hour timestamp against 30 days prior. 
	"""
	volunteer = models.ForeignKey(User)
	numHours = models.IntegerField()
	volDate = models.DateField()

	def was_submitted_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=30) <= self.volDate <= now

class Donors(models.Model):
	"""Donor information (name, donation amount, date of donation, and email) is stored here."""
	donorFirstName = models.CharField(max_length = 20, blank=False)
	donorLastName = models.CharField(max_length = 20, blank=False)
	donationAmount = models.IntegerField(blank = False)
	donorEmail =  models.CharField(max_length = 100, blank=False)
	donationDate = models.DateField('Date of Donation')
	
	def __str__(self):
        	return self.donorFirstName

class Incident_Report(models.Model):
	""" Information relevant to a critical incident report is stored here.
		Each model is linked to a residents unique ID. 
		- save:
			function saves the time that the model was created, and stores it in database. 
	"""
	DRUG = 'Drinking/Drug Use' 
	AWOL = 'AWOL'
	ALTERCATION = 'Altercation'
	INJURY = 'Injury'
	THEFT = 'Theft'
	VIOLATION = 'Violation of House Rule'
	TYPES = { 
		(DRUG, "Drinking/Drug Use"), 
		(AWOL, "AWOL"), 
		(ALTERCATION, "Altercation"),
		(INJURY, "Injury"),
	(THEFT, "Theft"),
	(VIOLATION, "Violation of House Rule")
	}
	staff = models.ManyToManyField(User)
	residents = models.ManyToManyField(Resident)
	incident_type = models.CharField('Type of Incident', 
					 max_length = 30,
					 choices = TYPES, default = None,
					 null=True, blank=True)
	comment = models.TextField('Comment')
	date_created = models.DateTimeField('Date Added')
	incident_date = models.DateTimeField('Date of Incident') 
	uniqueid = models.CharField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.date_created = timezone.now()
		return super(Incident_Report, self).save(*args, **kwargs)
