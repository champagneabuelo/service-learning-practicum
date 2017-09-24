from django.contrib import admin
from georgias.models import Incident_Report
from .models import Resident, Resident_Report, Interview_Report, Resident_Application, Termination_Report, Meeting_Report, Community_Program, Resident_Monthly_Report, Resident_Employment

admin.site.register(Resident)
admin.site.register(Resident_Report)
admin.site.register(Interview_Report)
admin.site.register(Resident_Application)
admin.site.register(Termination_Report)
admin.site.register(Meeting_Report)
admin.site.register(Community_Program)
admin.site.register(Resident_Monthly_Report)
admin.site.register(Resident_Employment)
admin.site.register(Incident_Report)

# Register your models here.
