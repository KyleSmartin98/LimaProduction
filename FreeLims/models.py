from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Sample(models.Model):
    SAMPLE_TYPE = (
        ('Solid', 'Solid'),
        ('Liquid', 'Liquid'),
        ('Powder', 'Powder')
    )
    SAMPLE_TEST = (
        ('Reverse Phase HPLC', 'Reverse Phase HPLC'),
        ('SEC HPLC', 'SEC HPLC'),
        ('UV-VIS', 'UV-VIS'),
        ('Moisture by Karl-Fischer', 'Moisture by Karl-Fischer'),
        ('pH', 'pH'),
        ('Dissolution', 'Dissolution'),
        ('Wet Chemistry', 'Wet Chemistry'),
        ('Raw Material', 'Raw Material'),
        ('CTL Testing', 'CTL Testing'),
    )
    organization = models.CharField(max_length=200)
    sample_name = models.CharField(max_length=100)
    sample_description = models.CharField(max_length=200)
    tracking_number = models.CharField(max_length=100)
    sample_volume = models.CharField(max_length=100)
    sample_quantity = models.IntegerField()
    sample_type = models.CharField(max_length=100, choices=SAMPLE_TYPE)
    expiration_date = models.CharField(max_length=100)
    logged_date = models.DateTimeField(default=datetime.now)
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)

    initiated = models.BooleanField(default=False) #Will determine if value is shown in initiated view
    sample_test = models.CharField(max_length=200, choices=SAMPLE_TEST, null=True)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_by', null=True)
    initiated_date = models.DateTimeField(default=datetime.now, null=True)

class Result(models.Model):
    PF = (
        (True, 'Pass'),
        (False, 'Fail')
    )
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateTimeField(default=datetime.now, null=True)
    result_pf = models.BooleanField(choices=PF, max_length=4, blank=True, default=None, null=True)
    sample_result = models.CharField(max_length=100, default=None, null=True)
    comments = models.CharField(max_length=200,  null=True, default=None)






