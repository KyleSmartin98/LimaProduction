from django.shortcuts import redirect, render
from .forms import SignUpForm, SampleForm, InitiateForm, ResultForm, InventoryForm, Qtyform, \
    OpenForm, editProfile, passwordChangeForm, privateKeyForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Sample, User, Cheminventory, Profile
from django.http import HttpResponse
import csv, shortuuid
from datetime import datetime
from .filters import SampleFilter, InventoryFilter, quickSampleFilter
import barcode
from barcode.writer import ImageWriter
from django.contrib.auth.decorators import login_required
from .utils import render_to_pdf
from django.core.mail import send_mail
from django.template import loader
from django.core.management.utils import get_random_secret_key

def landingPage(request):
    if request.method == "POST":
        contact_name = request.POST['contact-name']
        contact_email = request.POST['contact-email']
        contact_sub = request.POST['contact-subject']
        contact_message = request.POST['contact-message']

        send_mail(
            'Message From:'+ ' ' + contact_name + ' ' + ' ' + contact_email + ' ' + 'about' + ' ' + contact_sub,
            contact_message,
            contact_email,
            ['caretagus@gmail.com'],
            fail_silently=False,
        )

        context = {
            'contact_name': contact_name,
        }
        return render(request, 'FreeLims/landingpage.html', context)
    else:
        return render(request, 'FreeLims/landingpage.html')

@login_required(login_url='login')
def home(request):
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    samples = Sample.objects.filter(organization=user)
    inventories = Cheminventory.objects.filter(organization=user)
    mySampleFilter = quickSampleFilter(request.GET, queryset=samples)
    samples = mySampleFilter.qs
    page_title = 'GlobaLIMS-Home'

    context = {
        'samples': samples,
        'mySampleFilter': mySampleFilter,
        'inventories': inventories,
        'page_title': page_title
    }
    return render(request, 'FreeLims/home.html', context)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.", extra_tags='logout_message')
    return redirect('login')

def LogIn(request):
    form = SignUpForm()
    secretKeyForm = privateKeyForm()
    pass_form = passwordChangeForm(request.user)

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
                    messages.error(request, 'The Email Address and/or Password You Entered are Invalid. Please Try Again or Reset Your Password.', extra_tags='invalidpassword')
                    print('failed')
            if 'register' in request.POST:
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    Profile.objects.create(
                        user=user,
                        organization=form.cleaned_data['organization'],
                        email=form.cleaned_data['email'],
                    )
                    user.save()
                    profiles = Profile.objects.get(user=user)
                    if profiles.user is not None:
                        username = str(profiles.user)
                        email = profiles.email
                        organization = profiles.organization
                        secretKey = profiles.Secret_Key
                        email_body = "Thank you for signing up for GlobaLIMS, the future of lab management! Your organization is: " + organization + ' and your Secret Key is: ' + secretKey + ' Please keep this key in a secure location and never share it with anyone. This key will help you recover your account and change your password!'
                        email_subject = "Your GlobaLIMS Account is Registered!"
                        context = {
                            'organization': organization,
                            'secretKey': secretKey,
                            'username': username,
                        }
                        html_message = loader.render_to_string('FreeLims/registrationEmail.html', context)
                        send_mail(
                            email_subject,
                            email_body,
                            'caretagus@gmail.com',
                            [email],
                            fail_silently=True,
                            html_message=html_message
                        )
                        messages.success(request, 'Account was created for ' + username +
                                         '. Please check your email for your account information. ' +
                                         ' This is Your Secret Key You Must Copy This in a Secure Location: ' + secretKey)
                        return redirect('login')
            else:
                form = SignUpForm()
                print(form.errors, 'failed')
            if 'changepassword' in request.POST:
                privateKey = request.POST.get('privateKey')
                pass_form = passwordChangeForm(request.user, request.POST)
                if pass_form.is_valid():
                    profile = Profile.objects.get(Secret_Key=privateKey)
                    user = profile.user
                    u = User.objects.get(username=user)
                    new_password = request.POST.get('new_password1')
                    u.set_password(new_password)
                    u.save()
                    print('Passed')
                    messages.success(request, 'Your Password Has Been Updated!')
                    return redirect('login')
                else:
                    messages.error(request, 'Your New Password Was Unable to Be Saved!')
                    return redirect('login')


    context = {
        'form': form,
        'secretKeyForm': secretKeyForm,
        'pass_form': pass_form
    }
    return render(request, 'FreeLims/LogIn.html', context)

@login_required(login_url='login')
def settings_page(request):
    page_title = 'GlobaLIMS-Settings'
    profiles = Profile.objects.get(user=request.user.id)
    profileForm = editProfile(instance=profiles)
    secretKeyForm = privateKeyForm()
    pass_form = passwordChangeForm(request.user)
    pass
    if request.method == 'POST':
        if 'updateProfile' in request.POST:
            profileForm = editProfile(request.POST, instance=profiles)
            if profileForm.is_valid():
                obj = profileForm.save()
                obj.save
                messages.success(request, 'Your Profile Has Been Updated!', extra_tags="profile_updated")
                return redirect('settings')
        if 'updatePassword' in request.POST:
            privateKey = request.POST.get('privateKey')
            if privateKey == profiles.Secret_Key:
                pass_form = passwordChangeForm(request.user, request.POST)
                if pass_form.is_valid():
                    user = User.objects.get(id=request.user.id)
                    new_password = request.POST.get('new_password1')
                    user.set_password(new_password)
                    user.save()
                    print('Passed')
                    messages.success(request, 'Your Password Has Been Updated!', extra_tags='password_updated')
                    return redirect('settings')
                else:
                    messages.warning(request, 'Passwords do Not Match', extra_tags='incorrect_passwords')
                    print('failed')
            else:
                messages.warning(request, 'Your Secret Key is Incorrect', extra_tags='incorrect_privateKey')


    context = {
        'profiles': profiles,
        'profileForm': profileForm,
        'secretKeyForm': secretKeyForm,
        'pass_form': pass_form,
        'page_title': page_title
    }
    return render(request, 'FreeLims/settings.html', context)

@login_required(login_url='login')
def Sample_page(request):
    page_title='GlobaLIMS-Sample'
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    samples = Sample.objects.filter(organization=user)
    form = SampleForm()
    myfilter = SampleFilter(request.GET, queryset = samples)
    samples = myfilter.qs
    has_filters = any(field in request.GET for field in
                      set(myfilter.get_fields()))

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            obj = form.save(commit=False)
            obj.logged_by = user
            obj.organization = user.profile.organization
            #Profile.objects.get(user=User.objects.get('organization'))
            obj.save()
        else:
            print("ERROR : Form is invalid")
            print(form.errors)

    context = {
        'form': form,
        'samples': samples,
        'myfilter': myfilter,
        'has_filters': has_filters,
        'page_title': page_title,
               }
    return render(request, 'FreeLims/Sample.html', context)

@login_required(login_url='login')
def sampleBarcodeDownload(request, pk):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    sample = Sample.objects.get(id=pk)
    user = User.objects.get(pk=request.user.id)
    organization = user.profile.organization
    if sample.organization == organization:
        lot = str(sample.tracking_number)
        ean = barcode.get('Code128', f'{lot}', writer=ImageWriter())
        #ean.save(f'{lot}_Barcode')
        image = ean.render()
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        response['Content-Disposition'] = f'attachment; filename= "{lot}_barcode.png"'
        return response
    else:
        return redirect('Sample')

@login_required(login_url='login')
def sample_export(request):
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['sample name', 'sample description', 'tracking number', 'sample volume', 'sample quantity', 'sample type', 'expiration date'])
    for sample in Sample.objects.filter(organization=user).values_list('sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date'):
        writer.writerow(sample)
    response['Content-Disposition'] = f'attachment; filename= "Sample_{date_time}.csv"'

    return response

@login_required(login_url='login')
def Testing(request):
    page_title = 'GlobaLIMS-Sample Testing'
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    samples = Sample.objects.filter(organization=user)
    myfilter = SampleFilter(request.GET, queryset=samples)
    samples = myfilter.qs
    context = {
        'samples': samples,
        'myfilter': myfilter,
        'page_title': page_title,
    }
    return render(request, 'FreeLims/Testing.html', context)

@login_required(login_url='login')
def Initiatesample(request, pk):
    page_title = 'GlobaLIMS-Sample Initiation'
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    samples = Sample.objects.filter(organization=user)
    samplepk = Sample.objects.get(id=pk)
    myfilter = SampleFilter(request.GET, queryset=samples)
    samples = myfilter.qs
    form = InitiateForm(instance=samplepk)
    if samplepk.initiated == False:
        if samplepk.organization == user:
            if request.method == 'POST':
                form = InitiateForm(request.POST, instance=samplepk)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.initiated_by = User.objects.get(pk=request.user.id)
                    obj.initiated_date = str(datetime.now())
                    obj.save()
                    messages.success(request, 'Your Sample Initiation Form Has Been Saved!')
                    return redirect('Testing')
                else:
                    print("ERROR : Form is invalid")
                    print(form.errors)
        else:
                return redirect('Testing')
    else: return redirect('Testing')

    context = {
        'samples': samples,
        'form': form,
        'myfilter': myfilter,
        'page_title': page_title
    }
    return render(request, 'FreeLims/Testing.html', context)

@login_required(login_url='login')
def Results(request):
    page_title='GlobaLIMS-Result Reporting'
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    samples = Sample.objects.filter(organization=user)
    myfilter = SampleFilter(request.GET, queryset=samples)
    samples = myfilter.qs
    context = {
        'samples': samples,
        'myfilter': myfilter,
        'page_title': page_title,
    }
    return render(request, 'FreeLims/Results.html', context)

@login_required(login_url='login')
def Resultssubmit(request, pk):
    page_title='GlobaLIMS-Result Submission'
    samplepk = Sample.objects.get(id=pk)
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    samples = Sample.objects.filter(organization=user)
    myfilter = SampleFilter(request.GET, queryset=samples)
    samples = myfilter.qs
    form = ResultForm(instance=samplepk)
    if samplepk.organization == user:
        if samplepk.sample_result is None:
            if samplepk.initiated == True:
                if request.method == 'POST':
                    form = ResultForm(request.POST, instance=samplepk)
                    if form.is_valid():
                        obj = form.save(commit=False)
                        obj.reported_by = User.objects.get(pk=request.user.id)
                        obj.report_date = str(datetime.now())
                        obj.save()
                        messages.success(request, 'Your Result Submission Form Has Been Saved!')
                        return redirect('Results')
                    else:
                        print("ERROR : Form is invalid")
                        print(form.errors)
            else:
                return redirect('Results')
        else:
            return redirect('Results')
    else:
        return redirect('Results')
    context = {
        'form': form,
        'samples': samples,
        'myfilter': myfilter,
        'page_title': page_title
    }

    return render(request, 'FreeLims/Results.html', context)

@login_required(login_url='login')
def resultsSummary(request, pk, *args, **kwargs):
    page_title='GlobaLIMS-Result Summary Report'
    samples = Sample.objects.get(id=pk)
    now = datetime.now()
    user = User.objects.get(pk=request.user.id)
    organization = user.profile.organization
    tracking = str(samples.tracking_number)
    date_time = now.strftime("%m/%d/%Y")
    context = {
        'samples': samples,
        'now': date_time,
        'organization': organization,
        'page_title': page_title
    }
    if samples.organization == organization:
        if samples.sample_result is not None:
            pdf = render_to_pdf('FreeLims/resultSummary.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = tracking + "_" + date_time + ".pdf"
            content = "inline; filename= %s " %(filename)
            response['Content-Disposition'] = content
            return response
        else:
            return redirect('Results')
    else:
        return redirect('Results')

@login_required(login_url='login')
def result_export(request):
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['sample name', 'sample description', 'tracking number', 'sample volume', 'sample quantity', 'sample type', 'expiration date', 'sample test', 'sample result', 'report date'])
    for sample in Sample.objects.filter(organization=user).values_list('sample_name', 'sample_description', 'tracking_number', 'sample_volume', 'sample_quantity', 'sample_type', 'expiration_date', 'sample_test', 'sample_result', 'report_date'):
        writer.writerow(sample)
    response['Content-Disposition'] = f'attachment; filename= "Result_{date_time}.csv"'

    return response

@login_required(login_url='login')
def Trending(request):
    return render(request, 'FreeLims/Trending.html')

@login_required(login_url='login')
def Inventory(request):
    page_title='GlobaLIMS-Inventory'
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    inventories = Cheminventory.objects.filter(organization=user)
    myfilter = InventoryFilter(request.GET, queryset=inventories)
    inventories = myfilter.qs
    if request.method == 'POST':
        list_of_input_ids = request.POST.getlist('inputs')
        for i in list_of_input_ids:
            inventory = Cheminventory.objects.get(id=i)
            if inventory.open_container is True:
                Cheminventory.objects.filter(id=i).update(
                    inv_disposal = True,
                    disposal_by = User.objects.get(pk=request.user.id),
                    disposal_date = str(datetime.now())
                )
                return redirect('Inventory')


    context = {
        'inventories': inventories,
        'myfilter': myfilter,
        'page_title': page_title,
    }

    return render(request, 'FreeLims/Inventory.html', context)

@login_required(login_url='login')
def Inventorycreate(request):
    page_title='GlobaLIMS-Add Inventory'
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    inventories = Cheminventory.objects.filter(organization=user)
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
            user = User.objects.get(pk=request.user.id)
            obj = form.save(commit=False)
            if obj.quarantine is True:
                obj.open_container = False
            obj.logged_by = User.objects.get(pk=request.user.id)
            obj.logged_date = str(datetime.now())
            obj.quantity = str(1)
            obj.Lab_lot = f'GL{str(lot_id)}'
            obj.organization = user.profile.organization
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
        'page_title': page_title,
    }

    return render(request, 'FreeLims/Inventory.html', context)

@login_required(login_url='login')
def InventoryOpen(request, pk):
    page_title='GlobaLIMS-Open Inventory'
    inventorypk = Cheminventory.objects.get(id=pk)
    inventories = Cheminventory.objects.filter(id=pk)
    form = OpenForm(instance=inventorypk)
    user = User.objects.get(pk=request.user.id)
    organization = user.profile.organization
    if inventorypk.quarantine is False:
        #messages.error(request, 'This Reagent is Open')
        return redirect('Inventory')
    else:
        if inventorypk.organization == organization:
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
        else:
            return redirect('Inventory')

    context = {
        'form': form,
        'inventories': inventories,
        'page_title': page_title
    }

    return render(request, 'FreeLims/Inventory.html', context)

@login_required(login_url='login')
def BarcodeDownload(request, pk):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    inventory = Cheminventory.objects.get(id=pk)
    gl_lot = str(inventory.Lab_lot)
    user = User.objects.get(pk=request.user.id)
    organization = user.profile.organization
    gl_name = str(inventory.name)
    gl_expiry = str(inventory.expiry)
    if inventory.organization == organization:
        ean = barcode.get('Code128', f'{gl_lot}', writer=ImageWriter())
        #ean.save(f'{gl_lot}_Barcode')
        image = ean.render()
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        response['Content-Disposition'] = f'attachment; filename= "{gl_lot}_barcode.png"'
        return response
    else:
        return redirect('Inventory')

@login_required(login_url='login')
def inventory_export(request):
    user = User.objects.get(pk=request.user.id)
    user = user.profile.organization
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Reagent name', 'Reagent manufacturer', 'Reagent Lot', 'GlobaLIMS Lot', 'Expiry', 'Volume', 'Location', 'Logged Date'])
    for inventory in Cheminventory.objects.filter(organization=user).values_list('name', 'manufacturer', 'manufacturer_lot', 'Lab_lot', 'expiry', 'volume_size', 'location', 'logged_date'):
        writer.writerow(inventory)
    response['Content-Disposition'] = f'attachment; filename= "Inventory_{date_time}.csv"'
    return response

@login_required(login_url='login')
def Method(request):
    return render(request, 'FreeLims/Method.html')

