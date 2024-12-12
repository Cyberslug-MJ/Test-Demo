from django.contrib import admin
from . models import *

registry = [Announcements,subjects,StudentClasses,academic,Assessments,Student,staff,Guardian,Events,Assessment_records,subclasses,Approvals]
admin.site.register(registry)