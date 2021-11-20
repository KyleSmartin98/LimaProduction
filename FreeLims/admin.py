from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Sample)
"""admin.site.register(sample_initiated)
admin.site.register(sample_result)"""

