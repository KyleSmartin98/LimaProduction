from django.shortcuts import redirect
from .forms import SignUpForm, SampleForm, InitiateForm, ResultForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from .models import Sample, User
from django.http import HttpResponse
import csv
from datetime import datetime
from .filters import SampleFilter

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
    context = {
        'samples': samples,
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
    writer.writerow(['sample name', 'sample description', 'tracking number', 'sample volume', 'sample quantity', 'sample type', 'expiration date', 'sample_test', 'sample_result', 'report_date'])
    for sample in Sample.objects.all().values_list('sample name', 'sample description', 'tracking number', 'sample volume', 'sample quantity', 'sample type', 'expiration date', 'sample_test', 'sample_result', 'report_date'):
        writer.writerow(sample)
    response['Content-Disposition'] = f'attachment; filename= "Result_{date_time}.csv"'

    return response

def Trending(request):
    return render(request, 'FreeLims/Trending.html')

def Inventory(request):
    return render(request, 'FreeLims/Inventory.html')

def Method(request):
    return render(request, 'FreeLims/Method.html')

