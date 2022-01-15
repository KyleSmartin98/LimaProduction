from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.management.utils import get_random_secret_key

def generateHiddenKey():
    return get_random_secret_key()

class Profile(models.Model):
    ROLE = (
        ('Lab Technician','Lab Technician'),
        ('Manufacturing Technician', 'Manufacturing Technician'),
        ('Analyst','Analyst'),
        ('QC Analyst','QC Analyst'),
        ('Manufacturing Analyst','Manufacturing Analyst'),
        ('Lead Analyst','Lead Analyst'),
        ('Lead QC Analyst','Lead QC Analyst'),
        ('Lead Mfg Analyst','Lead Mfg Analyst'),
        ('Supervisor','Supervisor'),
        ('QC Supervisor', 'QC Supervisor'),
        ('Mfg Supervisor', 'Mfg Supervisor'),
        ('Manager', 'Manager'),
        ('QC Manager', 'QC Manager'),
        ('Mfg Manager', 'Mfg Manager'),
        ('Director', 'Director'),
        ('QC Director', 'QC Director'),
        ('Mfg Director', 'Mfg Director'),

    )
    DEPARTMENT = (
        ('','Department'),
        ('GENERAL LAB','GENERAL LAB'),
        ('QC CHEM','QC CHEM'),
        ('QC MICRO-BIO','QC MICRO-BIO'),
        ('QC BIO','QC BIO'),
        ('MANUFACTURING','MANUFACTURING')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default=None, null=True)
    last_name = models.CharField(max_length=100, default=None, null=True)
    empl_ID = models.CharField(max_length=100, default=None, null=True)
    organization = models.CharField(max_length=125, default=None, null=True)
    role = models.CharField(choices=ROLE, max_length=100, default=None, null=True)
    department = models.CharField(choices=DEPARTMENT, max_length=100, default=None, null=True)
    location = models.CharField(max_length=150, default=None, null=True)
    Secret_Key = models.CharField(max_length=100, default=generateHiddenKey)
    email = models.CharField(max_length=100, default=None, null=True)


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
    INITIATED = (
        (True, 'Initiate'),
        (False, 'Do Not Initiate')
    )
    PF = (
        (True, 'Pass'),
        (False, 'Fail')
    )

    sample_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    sample_description = models.CharField(max_length=200)
    tracking_number = models.CharField(max_length=100)
    sample_volume = models.CharField(max_length=100)
    sample_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    sample_type = models.CharField(max_length=100, choices=SAMPLE_TYPE)
    expiration_date = models.DateTimeField(default=None, max_length=100,  null=True)
    logged_date = models.DateTimeField(default=datetime.now)
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)

    initiated = models.BooleanField(choices=INITIATED,default=False) #Will determine if value is shown in initiated view
    sample_test = models.CharField(max_length=200, choices=SAMPLE_TEST, null=True)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='initiatedUser')
    initiated_date = models.DateTimeField(default=datetime.now, null=True)

    reported_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reportedUser')
    report_date = models.DateTimeField(default=datetime.now, null=True)
    result_pf = models.BooleanField(choices=PF, max_length=6, blank=True, default=None, null=True)
    sample_result = models.CharField(max_length=100, default=None, null=True)
    comments = models.CharField(max_length=200,  null=True, default=None)
    reference = models.CharField(max_length=200,  null=True, default=None)
    criteria = models.CharField(max_length=100, default=None, null=True)

    review_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reviewerUser')
    review_date = models.DateTimeField(default=datetime.now, null=True)


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
    QUARANTINE = (
        (True, 'Quarantine'),
        (False, 'Do Not Quarantine')
    )
    STATUS = (
        (True, 'Open'),
        (False, 'Close')
    )
    DISPOSAL = (
        (True, 'Disposed'),
        (False, 'Active')
    )
    logged_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    organization = models.CharField(max_length=125, default=None, null=True)
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

    quarantine = models.BooleanField(default=False, choices=QUARANTINE)
    open_container = models.BooleanField(choices=STATUS, blank=True, default=True, null=True)
    #open_date = models.DateTimeField(default=datetime.now, null=True)
    #open_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='openUser')

    inv_disposal = models.BooleanField(choices=DISPOSAL, blank=True, default=False, null=True)
    disposal_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='disposalUser')
    disposal_date = models.DateTimeField(default=datetime.now, null=True)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['expiry']




