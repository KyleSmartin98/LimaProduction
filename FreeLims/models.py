from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


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
    PF = (
        (True, 'Pass'),
        (False, 'Fail')
    )
    organization = models.CharField(max_length=200)
    sample_name = models.CharField(max_length=100)
    sample_description = models.CharField(max_length=200)
    tracking_number = models.CharField(max_length=100)
    sample_volume = models.CharField(max_length=100)
    sample_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    sample_type = models.CharField(max_length=100, choices=SAMPLE_TYPE)
    expiration_date = models.DateTimeField(default=None, max_length=100,  null=True)
    logged_date = models.DateTimeField(default=datetime.now)
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)

    initiated = models.BooleanField(default=False) #Will determine if value is shown in initiated view
    sample_test = models.CharField(max_length=200, choices=SAMPLE_TEST, null=True)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='initiatedUser')
    initiated_date = models.DateTimeField(default=datetime.now, null=True)

    reported_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reportedUser')
    report_date = models.DateTimeField(default=datetime.now, null=True)
    result_pf = models.BooleanField(choices=PF, max_length=4, blank=True, default=None, null=True)
    sample_result = models.CharField(max_length=100, default=None, null=True)
    comments = models.CharField(max_length=200,  null=True, default=None)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['expiration_date']
class Cheminventory(models.Model):
    MANUFACTURERS = (
        ('Fisher Scientific', 'Fisher Scientific'),
        ('ThermoFisher Scientific', 'ThermoFisher Scientific'),
        ('Acros Organic', 'Acros Organic'),
        ('Sigma-Aldrich', 'Sigma-Aldrich'),
        ('Agilent', 'Agilent'),
        ('MilliporeSigma', 'MilliporeSigma'),
        ('Mettler Toledo', 'Mettler Toledo'),
    )
    LOCATIONS = (
        ('General Lab Storage', 'General Lab Storage (25°C)'),
        ('Refrigerator', 'Refrigerator (2-8°C)'),
        ('Freezer', 'Freezer')
    )
    OPENCLOSE = (
        (True, 'Open'),
        (False, 'Close')
    )
    DISPOSAL = (
        (True, 'Disposed'),
        (False, 'Active')
    )
    logged_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    logged_date = models.DateTimeField(default=datetime.now, null=True)
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(choices=MANUFACTURERS, max_length=100)
    manufacturer_lot = models.CharField(max_length=100)
    expiry = models.DateTimeField(default=datetime.now, null=True)
    Lab_lot = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    volume_size = models.CharField(max_length=100)
    location = models.CharField(choices=LOCATIONS, max_length=100)
    comments = models.CharField(max_length=250)

    quarantine = models.BooleanField(default=False)
    open_container = models.BooleanField(choices=OPENCLOSE, blank=True, default=True, null=True)

    inv_disposal = models.BooleanField(choices=DISPOSAL, blank=True, default=False, null=True)
    disposal_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='disposalUser')
    disposal_date = models.DateTimeField(default=datetime.now, null=True)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['expiry']




