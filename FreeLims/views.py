from django.shortcuts import redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib import messages



def home(request):
    return render(request, 'FreeLims/home.html')

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

def Sample(request):
    return render(request, 'FreeLims/Sample.html')

def Testing(request):
    return render(request, 'FreeLims/Testing.html')

def Trending(request):
    return render(request, 'FreeLims/Trending.html')

