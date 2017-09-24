from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Textarea, extras
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from datetime import datetime
from .models import Resident, Resident_Application
from .models import Resident, Interview_Report, Resident_Report, Termination_Report, Meeting_Report, Resident_Employment, Community_Program
from .models import Resident_Report, Resident_Monthly_Report
import datetime


""" Code for forms (fields, field exclusion, formatting)  """

class ResidentForm(ModelForm):
    """ Resident application form -- first part of the application phase """
    date_of_birth = forms.DateField(widget= SelectDateWidget(years=[str(k) for k in range(datetime.datetime.now().year-100, datetime.datetime.now().year+1)]), initial = datetime.datetime.now())
    last_aa_na_meeting = forms.DateField(widget= SelectDateWidget(years=[str(k) for k in range(datetime.datetime.now().year-100, datetime.datetime.now().year+1)]), initial = datetime.datetime.now())
    class Meta:
        model = Resident_Application
        fields = ['resident_first',
                  'resident_last',
                  'date_of_birth',
                  'race',
                  'phone_number',
                  'mailing_address',
                  'physical_address',
                  'length_at_phys_addr',
                  'has_children',
                  'has_custody',
                  'is_married_or_relationship',
                  'spouse_name' ,
                  'spouse_age',
                  'level_of_education',
                  'is_receiving_income',
                  'has_va_license',
                  'uses_alcohol',
                  'uses_drugs' ,
                  'currently_sober' ,
                  'length_of_sobriety',
                  'ever_been_to_aa_na',
                  'aa_or_na',
                  'currently_in_aa_na',
                  'last_aa_na_meeting',
                  'currently_smokes',
                  'willing_to_quit',
                  'has_been_homeless',
                  'has_attempted_suicide',
                  'has_experienced_dom_violence',
                  'has_been_incarcerated',
                  'number_of_incar',
                  'currently_incar',
                  'on_probation',
                  'what_ghh_can_provide',
                  'benefits_from_residency',
                  'goals_in_months',
                  'obstacles_for_goals',
                  'applicant_attributes',
                  'applicant_essay'
        ]

        labels = {
            'resident_first' : _('Resident First Name'),
            'resident_last' : _('Resident Last Name'),
            'date_of_birth' : _('Date of Birth'),
            'race' : _('Race or Ethnicity'),
            'phone_number' : _('Phone Number'),
            'mailing_address' : _('Mailing Address'),
            'physical_address' : _('Physical Address'),
            'length_at_phys_addr' : _('How many years have you lived at this residence?'),
            'has_children' : _('Do you have any children?'),
            'has_custody' : _('Do you currently have custody of any children?'),
            'is_married_or_relationship' : _('Are you married or in a long term relationship?'),
            'spouse_name' : _('Spouse/Significant Other Name'),
            'spouse_age' : _('Spouse/Significant Other Age'),
            'level_of_education' : _('What is the highest level of education you have received?'),
            'is_receiving_income' : _('Are you working or receiving any income?'),
            'has_va_license' : _('Do you currently hold a valid VA drivers license?'),
            'uses_alcohol' : _('Alcohol?'),
            'uses_drugs' : _('Drugs?'),
            'currently_sober' : _('Are you currently sober?'),
            'length_of_sobriety' : _('If so, for how many days?'),
            'ever_been_to_aa_na' : _('Have you ever attended AA/NA or another substance abuse program?'),
            'aa_or_na' : _('If so, which one?'),
            'currently_in_aa_na' : _('Do you currently attend AA/NA?'),
            'last_aa_na_meeting' : _('If not, when was your last AA/NA meeting?'),
            'currently_smokes' : _('Do you smoke?'),
            'willing_to_quit' : _('Are you willing to quit? (Answer no if you already do not smoke)'),
            'has_been_homeless' : _('Have you ever experienced homelessness?'),
            'has_attempted_suicide' : _('Have you ever attempted suicide?'),
            'has_experienced_dom_violence' : _('Have you ever experienced domestic violence?'),
            'has_been_incarcerated' : _('Have you ever been incarcerated?'),
            'number_of_incar' : _('If so, how many times?'),
            'currently_incar' : _('Are you currently incarcerated?'),
            'on_probation' : _('Are you currently on probation?'),
            'what_ghh_can_provide' : _('What do you think GHH can provide for you?'),
            'benefits_from_residency' : _('What benefits will you receive from becoming a resident?'),
            'goals_in_months' : _('What goals do you hope to achieve in 3, 6, and 12 months from now?'),
            'obstacles_for_goals' : _('What obstacles or difficulties do you see in achieving your goals?'),
            'applicant_attributes' : _('What attributes do you possess that will make for a positive contribution to GHH residence/residents?'),
            'applicant_essay' : _('Applicant essay')
        }
        
             
        widgets = {
            'resident_first' : forms.TextInput(attrs={'class':"form-control"}),
            'resident_last' : forms.TextInput(attrs={'class':"form-control"}),
            'phone_number' : forms.TextInput(attrs={'class':"form-control",'placeholder':'XXX-XXX-XXXX','required':False}),
            'mailing_address' : forms.TextInput(attrs={'class':"form-control",'required':False}),
            'physical_address' : forms.TextInput(attrs={'class':"form-control",'required':False}),
            'length_at_phys_addr' : forms.NumberInput(attrs={'class':"form-control",'value':'0'}),
            'spouse_name' : forms.TextInput(attrs={'class':"form-control",'required':False}),
            'spouse_age' : forms.NumberInput(attrs={'class':"form-control",'value':'0'}),
            'length_of_sobriety' : forms.NumberInput(attrs={'class':"form-control",'value':'0'}),
            'number_of_incar' : forms.NumberInput(attrs={'class':"form-control",'value':'0'}),
            'what_ghh_can_provide' : Textarea(attrs={'class':"form-control",'required':False}),
            'benefits_from_residency' : Textarea(attrs={'class':"form-control",'required':False}),
            'goals_in_months' : Textarea(attrs={'class':"form-control",'required':False}),
            'obstacles_for_goals' : Textarea(attrs={'class':"form-control",'required':False}),
            'applicant_attributes' : Textarea(attrs={'class':"form-control",'required':False}),
            'applicant_essay' : Textarea(attrs={'class':"form-control",'required':False}),
            #'date_of_birth' : forms.SelectDateWidget(attrs={'class':"form-control"},years=[str(k) for k in range(datetime.datetime.now().year-100, datetime.datetime.now().year+1)]),
            #'last_aa_na_meeting' : forms.SelectDateWidget(attrs={'class':"form-control"},years=[str(k) for k in range(datetime.datetime.now().year-100, datetime.datetime.now().year+1)])
            #'date_of_birth' : extras.SelectDateWidget(years=[str(k) for k in range(1900, 2016)])                                                                                                         
        }
    

class TerminationForm(ModelForm):
        date = forms.DateField(widget= SelectDateWidget(years=[str(k) for k in range(datetime.datetime.now().year-100, datetime.datetime.now().year+1)]), initial = datetime.datetime.now())
        class Meta:
                model = Termination_Report
                widgets = {
                #       'date': forms.SelectDateWidget(years=[str(k) for k in range(datetime.datetime.now().year-10, datetime.datetime.now().year+1)], default=datetime.datetime.now()),                  
                }
                exclude = ['resident_first', 'resident_last', 'phase', 'race']


class MonthlyReportForm(ModelForm):
    month = forms.DateField(widget= SelectDateWidget(years=[str(k) for k in range(datetime.datetime.now().year-100, datetime.datetime.now().year+1)]), initial = datetime.datetime.now())

    class Meta:
        model = Resident_Monthly_Report
        widgets = {
        #               'month': forms.SelectDateWidget(years=[str(k) for k in range(datetime.datetime.now().year-10, datetime.datetime.now().year + 1)]),                                                
                }
        exclude = ['resident']

# Resident Interview Form
# Page 1
class InterviewForm1(ModelForm):
	""" This form portion will include:
		- last permanent address
		- emergency contact name
		- emergency contact relationship
 		- phone number
		- significant other name
		- custody of children 
		- source of income
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'job_history', 
			'job_skills',
			'valid_drivers_license', 
			'recent_arrests',
			'alcohol_history', 
			'prescription_history', 
			'opiates_history', 
			'cocaine_history',
			'marijuana_history',
			'others_history',
			'legal_consequences',
			'health_consequences',
			'family_social_consequences',
			'work_consequences',
			'sa_treatment',
			'sa_other_notes',
			'physical_abuse_history',
			'physical_abuse_comment',
			'emotional_abuse_history',
			'emotional_abuse_comment',
			'physicians_and_location',
			'medical_problems',
			'current_medications',
			'agencies_involved',
			'reference_name',
			'reference_relationship',
			'reference_phone',
			'level_of_education',
			'interest_in_further',
			'interest_skills_hobbies',
			'for_fun',
			'specific_goals'
		]

# Page 2
class InterviewForm2(ModelForm):
	""" This form portion will include:
		- job history
		- job skills
		- valid drivers license
		- recent arrests 
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'last_perm_address',
			'emergency_contact_name',
			'emergency_contact_relationship',
			'phone_number',
			'significant_other_name',
			'significant_other_relationship',
			'custody_of_children',
			'source_of_income',
			'alcohol_history',
			'prescription_history',
			'opiates_history',
			'cocaine_history',
			'marijuana_history',
			'others_history',
			'legal_consequences',
			'health_consequences',
			'family_social_consequences',
			'work_consequences',
			'sa_treatment',
			'sa_other_notes',
			'physical_abuse_history',
			'physical_abuse_comment',
			'emotional_abuse_history',
			'emotional_abuse_comment',
			'physicians_and_location',
			'medical_problems',
			'current_medications',
			'agencies_involved',
			'reference_name',
			'reference_relationship',
			'reference_phone',
			'level_of_education',
			'interest_in_further',
			'interest_skills_hobbies',
			'for_fun',
			'specific_goals'
		]
	labels = {
		'job_history' : mark_safe('Job History <p>'),
		'job_skills' : mark_safe('Job Skills <p>'),	
		'recent_arrests' : mark_safe('Recent Arrests <p>'),
	}
	widgets = {
    	'job_history' : Textarea(),
    	'job_skills' : Textarea(),
    	'recent_arrests' : Textarea(),
	}

# Page 3
class InterviewForm3(ModelForm):
	""" This form portion will include:
		- alcohol history
		- prescription history
		- opiates history
		- cocaine history
		- marijuana history
		- others history
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'last_perm_address',
			'emergency_contact_name',
			'emergency_contact_relationship',
			'phone_number',
			'significant_other_name',
			'significant_other_relationship',
			'custody_of_children',
			'source_of_income',
			'job_history',
			'job_skills',
			'valid_drivers_license',
			'recent_arrests',
			'legal_consequences',
			'health_consequences',
			'family_social_consequences',
			'work_consequences',
			'sa_treatment',
			'sa_other_notes',
			'physical_abuse_history',
			'physical_abuse_comment',
			'emotional_abuse_history',
			'emotional_abuse_comment',
			'physicians_and_location',
			'medical_problems',
			'current_medications',
			'agencies_involved',
			'reference_name',
			'reference_relationship',
			'reference_phone',
			'level_of_education',
			'interest_in_further',
			'interest_skills_hobbies',
			'for_fun',
			'specific_goals'
		]
	labels = {
		'alcohol_history' : mark_safe('Alcohol (Use, summary of amount, and last use) <p>'),
		'prescription_history' : 
				mark_safe(
					'Presription Drugs (Use, summary of amount, and last use) <p>'
				), 
		'opiates_history' : mark_safe('Opiates (Use, summary of amount, and last use) <p>'),
		'cocaine_history' : 
				mark_safe(
					'Cocaine (Use, summary of amount, and last use) <p>'
				),
		'marijuana_history' : 
				mark_safe(
					'Marijuana (Use, summary of amount, and last use) <p>'
				),
		'others_history' : mark_safe('Others (Use, summary of amount, and last use) <p>'),
	}
	widgets = {
	    'alcohol_history' : Textarea(),
    	'prescription_history' : Textarea(), 
    	'opiates_history' : Textarea(),
    	'cocaine_history' : Textarea(),
    	'marijuana_history' : Textarea(),
    	'others_history' : Textarea(),
	}

# Page 4
class InterviewForm4(ModelForm):
	""" This form portion will include:
		- legal consequences 
		- health consequences
		- family, social consequences
		- work consequences
		- SA treatment, other notes
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'last_perm_address',
			'emergency_contact_name',
			'emergency_contact_relationship',
			'phone_number',
			'significant_other_name',
			'significant_other_relationship',
			'custody_of_children',
			'source_of_income',
			'job_history',
			'job_skills',
			'valid_drivers_license',
			'recent_arrests',
			'alcohol_history',
			'prescription_history',
			'opiates_history',
			'cocaine_history',
			'marijuana_history',
			'others_history',
			'physical_abuse_history',
			'physical_abuse_comment',
			'emotional_abuse_history',
			'emotional_abuse_comment',
			'physicians_and_location',
			'medical_problems',
			'current_medications',
			'agencies_involved',
			'reference_name',
			'reference_relationship',
			'reference_phone',
			'level_of_education',
			'interest_in_further',
			'interest_skills_hobbies',
			'for_fun',
			'specific_goals'
		]
	labels = {
		'legal_consequences' : mark_safe('Legal Consequences <p>'),
		'health_consequences' : mark_safe('Health Consequences <p>'),
		'family_social_consequences' : mark_safe('Family and Social Consequences <p>'), 
		'work_consequences' : mark_safe('Work Consequences <p>'),
		'sa_treatment' : mark_safe('SA Treatment <p>'), 
		'sa_other_notes' : mark_safe('Other notes about SA <p>'),
	}
	widgets = {
    	'legal_consequences' : Textarea(), 
    	'health_consequences' : Textarea(),
    	'family_social_consequences' : Textarea(),
    	'work_consequences' : Textarea(), 
    	'sa_treatment' : Textarea(),
    	'sa_other_notes' : Textarea(),
	}

# Page 5
class InterviewForm5(ModelForm):
	""" This form portion will include:
		- physical abuse history
		- physical abuse comment
		- emotional abuse history
		- emotional abuse comment
		- physicians, locations
		- medical problems
		- current medications
		- agencies involved
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'last_perm_address',
			'emergency_contact_name',
			'emergency_contact_relationship',
			'phone_number',
			'significant_other_name',
			'significant_other_relationship',
			'custody_of_children',
			'source_of_income',
			'job_history',
			'job_skills',
			'valid_drivers_license',
			'recent_arrests',
			'alcohol_history',
			'prescription_history',
			'opiates_history',
			'cocaine_history',
			'marijuana_history',
			'others_history',
			'legal_consequences',
			'health_consequences',
			'family_social_consequences',
			'work_consequences',
			'sa_treatment',
			'sa_other_notes',
			'reference_name',
			'reference_relationship',
			'reference_phone',
			'level_of_education',
			'interest_in_further',
			'interest_skills_hobbies',
			'for_fun',
			'specific_goals'
		]
	labels = {
		'physical_abuse_comment' : mark_safe('Physical Abuse Comments <p>'),
		'emotional_abuse_comment' : mark_safe('Emotional Abuse Comments <p>'),
		'medical_problems' : mark_safe('Medical Problems <p>'),
	}
	widgets = {
	    'physical_abuse_comment' : Textarea(),
    	'emotional_abuse_comment' : Textarea(),
    	'medical_problems' : Textarea(),
	}

# Page 6
class InterviewForm6(ModelForm):
	""" This form portion will include:
		- reference name
		- reference relationship
		- reference phone
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'last_perm_address',
			'emergency_contact_name',
			'emergency_contact_relationship',
			'phone_number',
			'significant_other_name',
			'significant_other_relationship',
			'custody_of_children',
			'source_of_income',
			'job_history',
			'job_skills',
			'valid_drivers_license',
			'recent_arrests',
			'alcohol_history',
			'prescription_history',
			'opiates_history',
			'cocaine_history',
			'marijuana_history',
			'others_history',
			'legal_consequences',
			'health_consequences',
			'family_social_consequences',
			'work_consequences',
			'sa_treatment',
			'sa_other_notes',
			'physical_abuse_history',
			'physical_abuse_comment',
			'emotional_abuse_history',
			'emotional_abuse_comment',
			'physicians_and_location',
			'medical_problems',
			'current_medications',
			'agencies_involved',
			'level_of_education',
			'interest_in_further',
			'interest_skills_hobbies',
			'for_fun',
			'specific_goals'
		]
	labels = {
	}
	widgets = {
	}

# Page 7
class InterviewForm7(ModelForm):
	""" This form portion will include:
		- level of education
		- interest in futher 
		- interests, skills, hobbies
		- for fun
		- specific goals
	"""
	class Meta:
		model = Interview_Report
		exclude = [ 
			'last_perm_address',
			'emergency_contact_name',
			'emergency_contact_relationship',
			'phone_number',
			'significant_other_name',
			'significant_other_relationship',
			'custody_of_children',
			'source_of_income',
			'job_history',
			'job_skills',
			'valid_drivers_license',
			'recent_arrests',
			'alcohol_history',
			'prescription_history',
			'opiates_history',
			'cocaine_history',
			'marijuana_history',
			'others_history',
			'legal_consequences',
			'health_consequences',
			'family_social_consequences',
			'work_consequences',
			'sa_treatment',
			'sa_other_notes',
			'physical_abuse_history',
			'physical_abuse_comment',
			'emotional_abuse_history',
			'emotional_abuse_comment',
			'physicians_and_location',
			'medical_problems',
			'current_medications',
			'agencies_involved',
			'reference_name',
			'reference_relationship',
			'reference_phone'
		]
	labels = {
		'interest_in_further' :
			mark_safe(
				'Interest in pursuing further education or training <p>'
			), 
		'interest_skills_hobbies' : mark_safe('Interests, skills, and hobbies <p>'),
		'for_fun' : mark_safe('What do you do for fun? <p>'),
		'specific_goals' : mark_safe('Specific goals for the near future <p>'),
		'comment' : mark_safe('Comment <p>'),
	}
	widgets = {
    	'interest_in_further' : Textarea(),
    	'interest_skills_hobbies' : Textarea(),
    	'for_fun' : Textarea(),
    	'specific_goals' : Textarea(),
    	'comment' : Textarea(),
	}

# Old Interview form, will remove once new form is implemented
class InterviewForm(ModelForm): 
    class Meta:
        model = Interview_Report
	exclude = ['last_name', 'first_name', 'date_of_birth']
	labels = {
	'job_history' : mark_safe('Job History <p>'),
	'job_skills' : mark_safe('Job Skills <p>'),	
	'recent_arrests' : mark_safe('Recent Arrests <p>'),
	'alcohol_history' : mark_safe('Alcohol (Use, summary of amount, and last use) <p>'),
	'prescription_history' : 
			mark_safe(
				'Presription Drugs (Use, summary of amount, and last use) <p>'
			), 
	'opiates_history' : mark_safe('Opiates (Use, summary of amount, and last use) <p>'),
	'cocaine_history' : 
			mark_safe(
				'Cocaine (Use, summary of amount, and last use) <p>'
			),
	'marijuana_history' : 
			mark_safe(
				'Marijuana (Use, summary of amount, and last use) <p>'
			),
	'others_history' : mark_safe('Others (Use, summary of amount, and last use) <p>'), 
	'legal_consequences' : mark_safe('Legal Consequences <p>'),
	'health_consequences' : mark_safe('Health Consequences <p>'),
	'family_social_consequences' : mark_safe('Family and Social Consequences <p>'), 
	'work_consequences' : mark_safe('Work Consequences <p>'),
	'sa_treatment' : mark_safe('SA Treatment <p>'), 
	'sa_other_notes' : mark_safe('Other notes about SA <p>'),
	'physical_abuse_comment' : mark_safe('Physical Abuse Comments <p>'),
	'emotional_abuse_comment' : mark_safe('Emotional Abuse Comments <p>'),
	'medical_problems' : mark_safe('Medical Problems <p>'),
	'interest_in_further' :
			mark_safe(
				'Interest in pursuing further education or training <p>'
			), 
	'interest_skills_hobbies' : mark_safe('Interests, skills, and hobbies <p>'),
	'for_fun' : mark_safe('What do you do for fun? <p>'),
	'specific_goals' : mark_safe('Specific goals for the near future <p>'),
	'comment' : mark_safe('Comment <p>'),
	}	
	widgets = {
    	'job_history' : Textarea(),
    	'job_skills' : Textarea(),
    	'recent_arrests' : Textarea(),
    	'alcohol_history' : Textarea(),
    	'prescription_history' : Textarea(), 
    	'opiates_history' : Textarea(),
    	'cocaine_history' : Textarea(),
    	'marijuana_history' : Textarea(),
    	'others_history' : Textarea(),
    	'legal_consequences' : Textarea(), 
    	'health_consequences' : Textarea(),
    	'family_social_consequences' : Textarea(),
    	'work_consequences' : Textarea(), 
    	'sa_treatment' : Textarea(),
    	'sa_other_notes' : Textarea(),
    	'physical_abuse_comment' : Textarea(),
    	'emotional_abuse_comment' : Textarea(),
    	'medical_problems' : Textarea(), 
    	'interest_in_further' : Textarea(),
    	'interest_skills_hobbies' : Textarea(),
    	'for_fun' : Textarea(),
    	'specific_goals' : Textarea(),
    	'comment' : Textarea(),
	}
        
""" Report Form """        
class ReportForm(ModelForm):
    """ Form for reporting resident activities """
    class Meta: 
        model = Resident_Report
	widgets = {
	'date_added' : SelectDateWidget(years=[str(k) for k in range(2010, 2025)]),
	}
	labels = {
	'comment' : mark_safe('Comment: <p>'),
	}
        exclude = ['resident', 'uniqueid']

""" Resident Meeting Form """
class MeetingForm(ModelForm):
    """ Form for adding a meeting report for a resident """
    class Meta: 
        model = Meeting_Report
	widgets = {
	'meeting_date' : SelectDateWidget(years=[str(k) for k in range(2010, 2025)]),
	}
	labels = {
	'comment' : mark_safe('Comment: <p>'),
	}
        exclude = ['resident', 'uniqueid']

""" Community Program Form """
class CommunityProgramForm(ModelForm):
    """ Form for adding a community program report for a resident  """
    class Meta:
        model = Community_Program
        labels = {
        'program_name' : mark_safe('Program Name: <p>'),
	'description' : mark_safe('Description: <p>'),
	}
        exclude = ['resident', 'uniqueid']

""" Employment Form """        
class EmploymentForm(ModelForm): 
    """ Form for adding an employment history/status for a resident """
    class Meta: 
        model = Resident_Employment
        widgets = {
	'start_date' : SelectDateWidget(years=[str(k) for k in range(2010, 2025)]),
	'end_date' : SelectDateWidget(years=[str(k) for k in range(2010, 2025)]),
	}
        exclude = ['resident', 'uniqueid']
        
""" Application Form """
class ApplicationForm1(forms.Form):
    """Application Page 1 """
    app_first = forms.CharField(max_length=150)
    app_last = forms.CharField(max_length=150)
    app_dob = forms.DateField()
    app_mail_addr = forms.CharField(max_length=200)
    app_phys_addr = forms.CharField(max_length=200)

class ApplicationForm2(forms.Form):
    """ Aokucatuib Page 2 """
    subject = forms.CharField(max_length=200)

class ApplicationForm3(forms.Form):
    """ Application Page 3 """
    sender = forms.EmailField()
    
