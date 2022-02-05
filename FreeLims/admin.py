from django.contrib import admin

# Register your models here.

from .models import Sample, Cheminventory, Profile, Tenant

admin.site.register(Sample)
admin.site.register(Cheminventory)
admin.site.register(Profile)
admin.site.register(Tenant)


