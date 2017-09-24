from __future__ import unicode_literals

from django.db import models
from django import forms
from django.core.validators import RegexValidator

from datetime import datetime
import uuid

## All the database models for objects inm the residents portal

## RESIDENT TERMINATION REPORT ##
# termination report to keep track of terminated residents and reason for termination
class Termination_Report(models.Model):
    resident_first = models.CharField(max_length=20, default="") # resident first name
    resident_last = models.CharField(max_length=20, default="") # resident last name
    date = models.DateField('Date of Termination') # date of termination
    reason = models.TextField(max_length=100) # reason for termination
    race = models.CharField(max_length=100, default=None, null=None)
    phase = models.CharField(max_length=20, default=None) # resident's phase in application process
    
## RESIDENT'S INTERVIEW REPORT ##
# saves all data from interview
class Interview_Report(models.Model):
    # choices for education field
    LESS_THAN_HS = 'LTH'
    HS_OR_EQUIVALENT = 'HSE'
    SOME_COLLEGE_NO_DEGREE = 'SCN'
    POST_SECONDARY_NON_DEGREE_AWARD = 'PSN'
    ASSOCIATES_DEGREE = 'ADG'
    BACHELORS_DEGREE = 'BDG'
    MASTERS_DEGREE = 'MDG'
    DOCTORAL_OR_PROFESSIONAL_DEGREE = 'DPD'

    EDUCATION_CHOICES = (
        (LESS_THAN_HS, 'Less Than High School'),
        (HS_OR_EQUIVALENT, 'High School Diploma or Equivalent'),
        (POST_SECONDARY_NON_DEGREE_AWARD, 'Post Secondary Non-Degree Award'),
        (ASSOCIATES_DEGREE, 'Associates Degree'),
        (BACHELORS_DEGREE, 'Bachelors Degree'),
        (MASTERS_DEGREE, 'Masters Degree'),
        (DOCTORAL_OR_PROFESSIONAL_DEGREE, 'Doctoral or Professional Degree'),
        )

    # choices for y/n field
    YES_NO_CHOICE = (
	(True, 'Yes'),
	(False, 'No'),
    )

    # regex for phone number fields 
    phone_regex =  RegexValidator(regex=r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')    

	## PAGE 1 OF FORM ##
    last_perm_address = models.CharField(
				'Last Permanent Address', 
				default=None, 
				max_length=100, 
				blank=True,
				null=True
			)
 
    # TODO time at last address (in terms of months and years; will need multiple fields)
    
    emergency_contact_name = models.CharField(
				'Emergency Contact Name', 
				default=None, 
				max_length=30, 
				blank=True,
				null=True
			)

    emergency_contact_relationship = models.CharField(
				'Emergency Contact Relationship',
				default=None, 
				max_length=30, 
				blank=True,
				null=True
			)

    phone_number = models.CharField(
				'Phone Number', 
				default=None, 
				validators=[phone_regex], 
				max_length=12, 
				blank=True,
				null=True
			)

    significant_other_name = models.CharField(
				'Significant Other Name',
				default=None, 
				max_length=30, 
				blank=True,
				null=True
			)

    significant_other_relationship = models.CharField(
				'Significant Other Relationship', 
				default=None, 
				max_length=30, 
				blank=True,
				null=True
			)
    
    # TODO names and ages for children, dynamically add more children 
    custody_of_children = models.CharField(
				'Who has custody of children?', 
				default=None,
				null=True, 
				max_length=30
			)

    source_of_income = models.CharField(	
				'Source of Income', 
				default=None,
				null=True,
				max_length=30
			) 

	## PAGE 2 OF FORM ## 
    job_history = models.CharField(
					default=None, 
					null=True,
					max_length=30
			)

    job_skills = models.CharField(
					default=None, 
					null=True,
					max_length=30
			)

    valid_drivers_license = models.NullBooleanField(
				'Valid Drivers License?', 
				default=None,
				null=True,
				choices=YES_NO_CHOICE
			)
    
    # TODO criminal convictions with dates, time served, etc
    # TODO dynamic fields later, charfield for now
    recent_arrests = models.CharField(
				default=None, 
				null=True,
				max_length=30
			)


    ## PAGE 3 OF FORM ##
    alcohol_history = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    prescription_history = models.CharField(
				default=None,
				null=True,
				max_length=50
			)

    opiates_history = models.CharField(
				default=None,
				null=True,
				max_length=50
			)

    cocaine_history =  models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    marijuana_history = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)
 
    others_history = models.CharField(
				default=None,
				null=True,
				max_length=50
			)
 
    ## PAGE 4 OF FORM ##
    legal_consequences = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    health_consequences = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    family_social_consequences = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    work_consequences = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    sa_treatment = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    sa_other_notes = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)
   
	## PAGE 5 OF FORM ## 
    physical_abuse_history = models.NullBooleanField(
				'History of Physical Abuse?', 
				default=None,
				choices=YES_NO_CHOICE
			)

    physical_abuse_comment = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    emotional_abuse_history = models.NullBooleanField(
				'History of Emotional Abuse?',
				default=None,
				choices=YES_NO_CHOICE
			)

    emotional_abuse_comment = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    # TODO make multiple fields for physician and location
    physicians_and_location = models.CharField(
				'Physicians (with location)',
				default=None,
				null=True,
				max_length=50
			)

    medical_problems = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    current_medications = models.CharField(
				'Current Medications', 
				default=None,
				null=True, 
				max_length=50
			)
    
    agencies_involved = models.CharField(
				'Agencies currently involved with contact person', 
				default=None,
				null=True, 
				max_length=50
			)

    ## PAGE 6 OF FORM ## 
    reference_name = models.CharField(
				'Reference Name', 
				default=None, 
				null=True,
				max_length=30
			)
    
    reference_relationship = models.CharField(
				'Reference Relationship', 
				default=None, 
				null=True,
				max_length=20
			)

    reference_phone = models.CharField(
				'Reference Phone Number', 
				default=None, 
				null=True,
				validators=[phone_regex], 
				max_length=12, 
				blank=True
			)

	## PAGE 7 OF FORM ##
    level_of_education = models.CharField(
				'Highest Level of Education', 
				default=True,
				null=True,
				choices=EDUCATION_CHOICES, 
				max_length=30
			)

    interest_in_further = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    interest_skills_hobbies = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    for_fun = models.CharField(
				default=None, 
				null=True,
				max_length=50
			)

    specific_goals = models.CharField(
				default=None,
				null=True,
				max_length=50
			)

    comment = models.TextField()

    def get_all_int_fields(self):
		fields = []
		# save all interview fields into an array
		for f in self._meta.fields:
			fname = f.name
			get_choice = 'get_' + fname + '_display'
			if hasattr(self, get_choice):
				value = getattr(self, get_choice)()
			else:
                                value = getattr(self, fname)
			if f.editable and value:
				fields.append({
					'label': f.verbose_name,
					'name': f.name,
					'value': value
				})
		return fields

    def __str__(self):
        return self.comment
    
## RESIDENT ##

class Resident(models.Model):
    resident_first = models.CharField(max_length=20)
    resident_last = models.CharField(max_length=20)
    date_of_birth = models.DateField('Date of Birth')
    join_date = models.DateTimeField('Date Joined')
    race = models.CharField(max_length=100, default=None, null=None)
    uniqueid = models.UUIDField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True)
    interview_report = models.ForeignKey(Interview_Report, null=True, blank=True, default=None)
    validated = models.BooleanField(default=0)
    def __str__(self):
        return self.resident_first

## RESIDENT APPLICATION FORM ##
# all application fields

class Resident_Application(models.Model):
        # choices for y/n field
    YES_NO_CHOICE = (
	(True, 'Yes'),
	(False, 'No'),
    )

       # choices for education field
    LESS_THAN_HS = 'LTH'
    HS_OR_EQUIVALENT = 'HSE'
    SOME_COLLEGE_NO_DEGREE = 'SCN'
    POST_SECONDARY_NON_DEGREE_AWARD = 'PSN'
    ASSOCIATES_DEGREE = 'ADG'
    BACHELORS_DEGREE = 'BDG'
    MASTERS_DEGREE = 'MDG'
    DOCTORAL_OR_PROFESSIONAL_DEGREE = 'DPD'

    EDUCATION_CHOICES = (
        (LESS_THAN_HS, 'Less Than High School'),
        (HS_OR_EQUIVALENT, 'High School Diploma or Equivalent'),
        (POST_SECONDARY_NON_DEGREE_AWARD, 'Post Secondary Non-Degree Award'),
        (ASSOCIATES_DEGREE, 'Associates Degree'),
        (BACHELORS_DEGREE, 'Bachelors Degree'),
        (MASTERS_DEGREE, 'Masters Degree'),
        (DOCTORAL_OR_PROFESSIONAL_DEGREE, 'Doctoral or Professional Degree'),
        )

    # ethnicity/race options
    NUL = '---'
    AMAL = 'American Indian or Alaska Native'
    AS = 'Asian'
    BL = 'Black or African American'
    HPI = 'Native Hawaiian or Other Pacific Islander'
    WH = 'White'
    HI = "Hispanic or Latino"
    OTH = "Other"
    RACES = {
        (NUL, '---'),
        (BL, 'Black or African American'),
        (WH, 'White'),
        (AMAL, 'American Indian or Alaska Native'),
        (AS, 'Asian'),
        (HPI, 'Native Hawaiian or Other Pacific Islander'),
        (HI, "Hispanic or Latino"),
        (OTH, "Other")
    }
    
    # organization options
    BOTH = 'Both'
    AA = 'AA'
    NA = 'NA'

    GROUP_CHOICES = {
        (NUL, '---'),
        (BOTH, 'Both'),
        (AA, 'AA'),
        (NA, 'NA')
        }

     # regex for phone number fields 
    phone_regex =  RegexValidator(regex=r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    
    # application fields
    phone_regex =  RegexValidator(regex=r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    resident_first = models.CharField(max_length=150, default=None, blank=False, null=False)
    resident_last = models.CharField(max_length=150, default=None, blank=False, null=False)
    date_of_birth = models.DateField('Date of Birth')
    race = models.CharField(max_length=100, choices = RACES, default=None)
    email = models.CharField(max_length=254, default=None, blank=True, null=True)
    phone_number = models.CharField(default=None, validators=[phone_regex], max_length=18, blank=True,null=True)
    mailing_address = models.CharField(default=None, max_length=100, blank=True,null=True)
    physical_address = models.CharField(default=None, max_length=100, blank=True,null=True)
    length_at_phys_addr = models.IntegerField(blank=True, null=True)
    level_of_education = models.CharField(default=None,choices=EDUCATION_CHOICES, max_length=30, blank=False, null=False)
    has_children = models.BooleanField(default=False)
    has_custody = models.BooleanField(default=False)
    is_married_or_relationship = models.BooleanField(default=False)
    spouse_name = models.CharField(max_length= 150, default=None, blank=True, null=True)
    spouse_age = models.IntegerField(blank=True, null=True)
    level_of_education = models.CharField(default=None,null=True,choices=EDUCATION_CHOICES, max_length=30)
    is_receiving_income = models.BooleanField(default=False)
    has_va_license = models.BooleanField(default=False)
    uses_alcohol = models.BooleanField(default=False)
    uses_drugs = models.BooleanField(default=False)
    currently_sober = models.BooleanField(default=False)
    length_of_sobriety = models.IntegerField(blank=True, null=True)
    ever_been_to_aa_na = models.BooleanField(default=False)
    aa_or_na = models.CharField(max_length=30, default=None,blank=False, null=False, choices=GROUP_CHOICES)
    currently_in_aa_na = models.BooleanField(default=False)
    last_aa_na_meeting = models.DateField(blank=True, null=True)
    currently_smokes = models.BooleanField(default=False)
    willing_to_quit = models.BooleanField(default=False)
    has_been_homeless = models.BooleanField(default=False)
    has_attempted_suicide = models.BooleanField(default=False)
    has_experienced_dom_violence = models.BooleanField(default=False)
    has_been_incarcerated = models.BooleanField(default=False)
    number_of_incar = models.IntegerField(blank=True, null=True)
    currently_incar = models.BooleanField(default=False)
    on_probation = models.BooleanField(default=False)
    what_ghh_can_provide = models.TextField(default=None)
    benefits_from_residency = models.TextField(default=None)
    goals_in_months = models.TextField(default=None)
    obstacles_for_goals = models.TextField(default=None)
    applicant_attributes = models.TextField(default=None)
    applicant_essay = models.TextField(default=None)
    uniqueid = models.CharField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True)
    interview_report = models.ForeignKey(Interview_Report, null=True, blank=True, default=None)

    def __str__(self):
        return self.resident_first
    
    
class Terminated_Resident(models.Model):
    resident = resident = models.ForeignKey(Resident)
    resident_first = models.CharField(max_length=20, default="") # resident first name
    resident_last = models.CharField(max_length=20, default="") # resident last name
    date = models.DateField('Date of Termination') # date of termination
    reason = models.TextField(max_length=100) # reason for termination
    race = models.CharField(max_length=100, default=None)
    phase = models.CharField(max_length=20, default=None) # resident's phase in application process

## RESIDENT MEETING REPORT ##
# 
class Meeting_Report(models.Model):
    # Meeting type options
    AA = 'Alcoholics Anonymous' 
    NA = 'Narcotics Anonymous'
    HOUSE = 'House Meeting'
    OTHER = 'Other'
    MEETING_TYPES = { 
        (AA, "AA (Alcoholics Anonymous)"),
        (NA, "NA (Narcotics Anonymous)"), 
        (HOUSE, "House Meeting"),
        (OTHER, "Other"),
    }
    
    resident = models.ForeignKey(Resident) # resident associated with meeting report
    meeting_type = models.CharField('Type of Meeting', 
				     max_length = 30,
                     choices = MEETING_TYPES, default = None,
				     null=True, blank=True) # type of meeting
    comment = models.TextField('Comments', max_length = 100) # additional comments
    meeting_date = models.DateField('Meeting Date') # date of meeting
    uniqueid = models.CharField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True) # meeting report id
    
    def __str__(self):
        return self.resident.resident_first

## RESIDENT COMMUNITY PROGRAM REPORT ## 
# resident's community program involvement
class Community_Program(models.Model):
    resident = models.ForeignKey(Resident) # resident associated with community program report
    program_name = models.TextField('Program Name', max_length = 50) # community program name
    description = models.TextField('Description', max_length = 400) # description of what they do
    uniqueid = models.CharField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True) # community program id
    
    def __str__(self):
        return self.resident.resident_first
    
## RESIDENT EMPLOYMENT REPORT ## 
# residents' employment history
class Resident_Employment(models.Model):
    resident = models.ForeignKey(Resident) # resident associated with employment report
    employer = models.TextField('Employer', max_length = 30) # employer of the resident
    position = models.TextField('Position', max_length = 30) # what position(s) did the ydo
    start_date = models.DateField('Start Date') # date they were employed
    end_date = models.DateField('End Date') # date they quit
    uniqueid = models.CharField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True) # employment program id
    
    def __str__(self):
        return self.resident.resident_first

## RESIDENT MONTHLY REPORT ##
class Resident_Monthly_Report(models.Model):
    resident = models.ForeignKey(Resident)
    month = models.DateField('Filter', default = None)
    
## RESIDENT REPORT ##
# report for resident's activities 
class Resident_Report(models.Model):
    # types of activities
    JOB = 'Job Shift' 
    INTERVIEW = 'Interview'
    THERAPY = 'Therapy'
    COURT = 'Court'
    ACTIVITY_TYPES = { 
        (JOB, "Job"), 
        (INTERVIEW, "Interview"), 
        (THERAPY, "Therapy Visit"),
        (COURT, "Court Date"),
    }
    resident = models.ForeignKey(Resident) # resident associated with the report
    activity_type = models.CharField('Type of Activity', 
				     max_length = 30,
                     choices = ACTIVITY_TYPES, default = None,
				     null=True, blank=True) # type of activity
    comment = models.TextField('Comment', max_length = 100) # description of the activity
    date_added = models.DateTimeField('Date Added') # date report was added
    uniqueid = models.CharField(default=uuid.uuid4, unique=True, max_length=100, null=True, blank=True) # report id
    
    def __str__(self):
        return self.resident.resident_first


    



