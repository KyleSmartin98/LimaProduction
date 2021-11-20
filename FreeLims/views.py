from django.shortcuts import redirect
from .forms import SignUpForm, SampleForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from .models import Sample


def home(request):
    return render(request, 'FreeLims/home.html')
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')
def LogIn(request):
    form = SignUpForm()
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

def Inventory(request):
    return render(request, 'FreeLims/Inventory.html')

def Method(request):
    return render(request, 'FreeLims/Method.html')

def Results(request):
    return render(request, 'FreeLims/Results.html')

def Sample_page(request):
    samples = Sample.objects.all()
    form = SampleForm()

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form, 'samples': samples
               }
    return render(request, 'FreeLims/Sample.html', context)

def Testing(request):
    return render(request, 'FreeLims/Testing.html')

def Trending(request):
    return render(request, 'FreeLims/Trending.html')

