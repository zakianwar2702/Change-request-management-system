from django.contrib import admin
from .models import ChangeRequest, DeveloperAssignment

admin.site.register(ChangeRequest)
admin.site.register(DeveloperAssignment)