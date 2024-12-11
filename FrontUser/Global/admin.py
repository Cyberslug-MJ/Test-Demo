from django.contrib import admin
from . models import *

registry = [Announcements,subjects,StudentClasses,academic,Assessments,Student,staff,Guardian,Events,Assessment_records]
admin.site.register(registry)