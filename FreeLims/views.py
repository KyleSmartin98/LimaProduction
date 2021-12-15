from django.shortcuts import redirect
from .forms import SignUpForm, SampleForm, InitiateForm, ResultForm, InventoryForm, Qtyform, DisposeForm, \
    OpenForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from .models import Sample, User, Cheminventory
from django.http import HttpResponse
import csv, shortuuid
from datetime import datetime
from .filters import SampleFilter, InventoryFilter
import barcode
from PIL import Image
from barcode.writer import ImageWriter


def home(request):
    return render(request, 'FreeLims/home.html')

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

def LogIn(request):
    form = SignUpForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            if 'login' in request.POST:
                username = request.POST.get('username1')
                password = request.POST.get('password1')
                new_user = authenticate(request, username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                    return redirect('home')
                else:
                    print('failed')
            if 'register' in request.POST:
                form = SignUpForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)
            else: print(form.errors)

    context = {'form': form}
    return render(request, 'FreeLims/LogIn.html', context)

def Sample_page(request):
    samples = Sample.objects.all()
    form = SampleForm()

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.logged_by = User.objects.get(pk=request.user.id)
            obj.save()
        else:
            print("ERROR : Form is invalid")
            print(form.errors)

    myfilter = SampleFilter(request.GET, queryset = samples)
    samples = myfilter.qs
    has_filters = any(field in request.GET for field in
                      set(myfilter.get_fields()))

    context = {
        'form': form,
        'samples': samples,
        'myfilter': myfilter,
        'has_filters': has_filters,
               }
    return render(request, 'FreeLims/Sample.html', context)

def sample_export(request):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['sample name', 'sample description', 'tracking number', 'sample volume', 'sample quantity', 'sample type', 'expiration date'])
    for sample in Sample.objects.all().values_list('sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date'):
        writer.writerow(sample)
    response['Content-Disposition'] = f'attachment; filename= "Sample_{date_time}.csv"'

    return response

def Testing(request):
    samples = Sample.objects.all()
    myfilter = SampleFilter(request.GET, queryset=samples)
    samples = myfilter.qs
    context = {
        'samples': samples,
        'myfilter': myfilter,
    }
    return render(request, 'FreeLims/Testing.html', context)

def Initiatesample(request, pk):
    samplepk = Sample.objects.get(id=pk)
    samples = Sample.objects.all()
    form = InitiateForm(instance=samplepk)
    if request.method == 'POST':
        form = InitiateForm(request.POST, instance=samplepk)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.initiated_by = User.objects.get(pk=request.user.id)
            obj.initiated_date = str(datetime.now())
            obj.save()
            return redirect('Testing')
        else:
            print("ERROR : Form is invalid")
            print(form.errors)
    context = {
        'samples': samples,
        'form': form,
    }
    return render(request, 'FreeLims/Testing.html', context)

def Results(request):
    samples = Sample.objects.all()
    myfilter = SampleFilter(request.GET, queryset=samples)
    samples = myfilter.qs
    context = {
        'samples': samples,
        'myfilter': myfilter,
    }
    return render(request, 'FreeLims/Results.html', context)

def Resultssubmit(request, pk):
    samplepk = Sample.objects.get(id=pk)
    samples = Sample.objects.all()
    form = ResultForm(instance=samplepk)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=samplepk)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.reported_by = User.objects.get(pk=request.user.id)
            obj.report_date = str(datetime.now())
            obj.save()
            return redirect('Results')
        else:
            print("ERROR : Form is invalid")
            print(form.errors)

    context = {
        'form': form,
        'samples': samples,
    }

    return render(request, 'FreeLims/Results.html', context)

def result_export(request):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['sample name', 'sample description', 'tracking number', 'sample volume', 'sample quantity', 'sample type', 'expiration date', 'sample test', 'sample result', 'report date'])
    for sample in Sample.objects.all().values_list('sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date', 'sample_test', 'sample_result', 'report_date'):
        writer.writerow(sample)
    response['Content-Disposition'] = f'attachment; filename= "Result_{date_time}.csv"'

    return response

def Trending(request):
    return render(request, 'FreeLims/Trending.html')

def Inventory(request):
    inventories = Cheminventory.objects.all()
    myfilter = InventoryFilter(request.GET, queryset=inventories)
    inventories = myfilter.qs
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('inputs')
        for i in list_of_input_ids:
            Cheminventory.objects.filter(id=i).update(inv_disposal=True)
            return redirect('Inventory')

    context = {
        'inventories': inventories,
        'myfilter': myfilter,
    }

    return render(request, 'FreeLims/Inventory.html', context)

def Inventorycreate(request):
    inventories = Cheminventory.objects.all()
    form = InventoryForm()
    qtyform = Qtyform()
    id = shortuuid.ShortUUID(alphabet="0123456789")
    lot_id = id.random(length=7)
    myfilter = InventoryFilter(request.GET, queryset=inventories)
    inventories = myfilter.qs
    if request.method == 'POST':
        qty = request.POST.get('quantity')
        form = InventoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.quarantine is True:
                obj.open_container = False
            obj.logged_by = User.objects.get(pk=request.user.id)
            obj.logged_date = str(datetime.now())
            obj.quantity = str(1)
            obj.Lab_lot = f'GL{str(lot_id)}'
            for i in range(int(qty)):
                obj.pk = None
                obj.save()
        else:
            print("ERROR : Form is invalid")
            print(form.errors)

    context = {
        'inventories': inventories,
        'form': form,
        'qtyform': qtyform,
        'myfilter': myfilter,
    }

    return render(request, 'FreeLims/Inventory.html', context)

def InventoryOpen(request, pk):
    inventorypk = Cheminventory.objects.get(id=pk)
    inventories = Cheminventory.objects.filter(id=pk)
    form = OpenForm(instance=inventorypk)
    if inventorypk.quarantine is False:
        messages.error(request, 'This Reagent is Open')
        return redirect('Inventory')
    else:
        if request.method == 'POST':
            form = OpenForm(request.POST, instance=inventorypk)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.quarantine = False
                obj.open_container = True
                obj.save()
                return redirect('Inventory')
            else:
                print("ERROR : Form is invalid")
                print(form.errors)

    context = {
        'form': form,
        'inventories': inventories,
    }

    return render(request, 'FreeLims/Inventory.html', context)

def BarcodeDownload(request, pk):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    inventory = Cheminventory.objects.get(id=pk)
    gl_lot = str(inventory.Lab_lot)
    gl_name = str(inventory.name)
    gl_expiry = str(inventory.expiry)
    ean = barcode.get('Code128', f'{gl_lot}', writer=ImageWriter())
    ean.save(f'{gl_lot}_Barcode')
    image = ean.render()
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response

def inventory_export(request):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Reagent name', 'Reagent manufacturer', 'Reagent Lot', 'GlobaLIMS Lot', 'Expiry', 'Volume', 'Location', 'Logged Date'])
    for inventory in Cheminventory.objects.all().values_list('name', 'manufacturer', 'manufacturer_lot', 'Lab_lot', 'expiry', 'volume_size', 'location', 'logged_date'):
        writer.writerow(inventory)
    response['Content-Disposition'] = f'attachment; filename= "Inventory_{date_time}.csv"'
    return response



def Method(request):
    return render(request, 'FreeLims/Method.html')

