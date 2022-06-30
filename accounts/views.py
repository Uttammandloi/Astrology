import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from regex import R
from accounts.models import Birthdata, RateyourReading, Contact
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from geopy.geocoders import Nominatim
from datetime import datetime
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt




# Create your views here.


def home(request):
    current_user = request.user
    user_id = current_user.id
    # print(user_id)
    return render(request, 'index.html',)


def registration(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not firstname:
            messages.error(request, 'first name is required')
            return redirect('registration')
        elif not username:
            messages.error(request, 'user name is required')
            return redirect('registration')
        elif not email:
            messages.error(request, 'email name is required')
            return redirect('registration')
        elif not password:
            messages.error(request, 'password is required')
            return redirect('registration')
        elif not confirm_password:
            messages.error(request, 'confirm password is required')
            return redirect('registration')

        if password == confirm_password:
            error = False
            if User.objects.filter(username=username).exists():
                error = True
                messages.error(request, 'user is already exists!')
                return redirect('registration')
            if User.objects.filter(email=email).exists():
                error = True
                messages.error(request, 'email is already exists!')
                return redirect('registration')
            if error == False:
                user = User.objects.create_user(
                    first_name=firstname, username=username, email=email, password=password)
                user.save()
                messages.success(request, 'You are register successfully!')
                return redirect('login')
        else:
            messages.error(request, 'password do not match!')
            return redirect('registration')
    else:
        return render(request, 'registration.html',)


def login(request):
    
    if 'token' in request.session:
        return redirect('userdashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        if not username:
            messages.error(request, 'Username and password is required')
            return redirect('login')
        
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_superuser==True:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)  
            request.session['user_name'] = user.username
            request.session['token'] = 'mytoken' + user.username
            messages.success(request, 'You have logged in sucessfully')
            return redirect('userdashboard')
        
        else:
            messages.error(
                request, 'Invalid username or password.')

            return redirect('login')

    return render(request, "login.html")


def userdashboard(request):
    if 'token' not in request.session:
        return redirect('login')
    return render(request, 'userdashboard.html',)


def logout(request):
    del request.session['token']
    messages.success(request, 'Logout successfully.')
    return redirect('login')


def birthdata(request):
    current_user = request.user
    user_id = current_user.id
    if 'token' not in request.session:
        return redirect('login')

    if request.method == 'POST':

        birthdata = Birthdata()
        # calling the Nominatim tool
        loc = Nominatim(user_agent="GetLoc")
        city = request.POST.get('birth_city_sate')
        getLoc = loc.geocode(city)
        lat = getLoc.latitude
        long = getLoc.longitude
        birthdata.screen_name = request.POST.get('screen_name')
        birthdata.full_name = request.POST.get('full_name')
        birthdata.user_id = request.POST.get('user_id')
        birthdata.date_of_birth = request.POST.get('date_of_birth')
        birthdata.time_of_birth = request.POST.get('time_of_birth')
        s = datetime.strptime(birthdata.time_of_birth, "%H:%M")
        birth_time = s.strftime("%I:%M %p")
        birthdata.birth_city_sate = request.POST.get('birth_city_sate')
        birthdata.longitude = str(long)
        birthdata.lattitude = str(lat)

        birthdata.your_current_location = request.POST.get(
            'your_current_location')
        birthdata.transits_chart_date = request.POST.get('transits_chart_date')
        birthdata.email = request.POST.get('email')
        birthdata.cell_number = request.POST.get('cell_number')
        birthdata.message = request.POST.get('message')
        birthdata.save()
        birthdata = Birthdata()
        # return redirect('/birthdata')
        
        # configure your email address
        # step1:
        email_user = 'uttam.synetalsolutions@gmail.com'
        email_password = 'aexqwqejdextcaer'
        email_send = 'uttam.synetalsolutions@gmail.com'

        # step2:
        # https://myaccount.google.com/lesssecureapps
        # Allow less secure apps: ON (remember you must be on for sending email)

        subject = 'Contact Information'
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        msg.attach(MIMEText('<html><body><p>Hi Admin, <br> PFA</p><h4>Thanks & Regards</h4><p>'+ birthdata.screen_name+'</p></body></html>', 'html', 'utf-8'))

        filename = 'text.cin'

        with open(filename, "w+") as file1:
            L = ["NM1:", birthdata.full_name, '\n', "DT1:", str(birthdata.date_of_birth), '\n', "TM1:", str(birth_time), '\n', "PL1:", birthdata.birth_city_sate,
                 '\n', "LONG1: ", str(birthdata.longitude), '\n', "LAT1: ", str(birthdata.lattitude), '\n', "TDATE:", str(birthdata.transits_chart_date), '\n', "DONE:"]
            file1.writelines(L)
            file1.close()
            
        with open(filename, "r") as f:
            part = MIMEApplication(f.read(), Name=basename(filename))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(
            basename(filename))
        msg.attach(part)

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_send, text)
        server.quit()
        if os.path.isfile(filename):
            os.remove(filename)
    return render(request, 'birthdata.html', {'user_id': user_id})



def readingrate(request):
    current_user = request.user
    user_id = current_user.id
    if 'token' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        rate_your_reading = RateyourReading()

        rate_your_reading.screen_name = request.POST.get('screen_name')
        rate_your_reading.user_id = request.POST.get('user_id')
        rate_your_reading.email = request.POST.get('email')
        rate_your_reading.rate_synchronic = request.POST.get(
            'rate_your_synchronicity')
        rate_your_reading.message = request.POST.get('message')
        rate_your_reading.save()

        # configure your email address
        # step1:
        email_user = 'uttam.synetalsolutions@gmail.com'
        email_password = 'aexqwqejdextcaer'
        email_send = 'uttam.synetalsolutions@gmail.com'

        # step2:
        # https://myaccount.google.com/lesssecureapps
        # Allow less secure apps: ON (remember you must be on for sending email)

        subject = 'Contact Information'
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        msg.attach(MIMEText('<html><body>' + "<h2>Thanks And Regards</h2><hr>" + "<br><br>" +
                            "<h3>BASIC INFO</h3>" + "<strong>User/Screen Name : </strong>" + rate_your_reading.screen_name +
                            '<br><strong> Email Address: </strong>' + rate_your_reading.email + '<br><strong> Rate Your Synchronicity : </strong>' +
                            rate_your_reading.rate_synchronic + '<br><strong> Feedback Message: </strong>' + rate_your_reading.message + "</html></body>", 'html', 'utf-8'))
        

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_send, text)
        server.quit()
    
    return render(request, 'readingrate.html', {'user_id': user_id})


def changepassword(request):
    if 'token' not in request.session:
        return redirect('login')
    return render(request, 'changepassword.html',)




def contact(request):
    if 'token' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact.name = name
        contact.email = email
        contact.message = message
        contact.save()
        # configure your email address
        # step1:
        email_user = 'uttam.synetalsolutions@gmail.com'
        email_password = 'aexqwqejdextcaer'
        email_send = 'uttam.synetalsolutions@gmail.com'

        # step2:
        # https://myaccount.google.com/lesssecureapps
        # Allow less secure apps: ON (remember you must be on for sending email)

        subject = 'Contact Information'
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        msg.attach(MIMEText('<html><body><p>Hi Admin, <br> PFA</p><h4>Thanks & Regards</h4><p>'+ contact.name+'</p></body></html>', 'html', 'utf-8'))
        filename = 'text.cin'
   
        with open(filename, "w+") as file1:
            L = ["Name: ", contact.name, '\n', "Email: ",
                 contact.email, '\n', "message: ", contact.message, '\n']
            file1.writelines(L)
            file1.close()
        with open(filename, "r") as f:
            part = MIMEApplication(f.read(), Name=basename(filename))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(
            basename(filename))
        msg.attach(part)

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_send, text)
        server.quit()
        if os.path.isfile(filename):
            os.remove(filename)
        messages.success(request, 'messege sent sucessfully')
        return redirect('contact')

    return render(request, 'contact.html',)


def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password changed sucessfully')
                return redirect('login')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'changpass.html', {'form': fm})
    else:
        return redirect('login')



# Backend dashboard..

@csrf_exempt
def backend_dashboard_login(request):
    if 'tokenadmin' in request.session:
        return redirect('backend')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not username:
            messages.error(request, 'Username and password is required')
            return redirect('backendlogin')
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_superuser==True:
                auth.login(request, user)
                request.session['user_name'] = user.username
                request.session['tokenadmin'] = 'mytokens' + user.username
                # messages.success(request, 'You have logged in sucessfully')
                return redirect('backend')
        else:
            messages.error(
                request, 'Invalid username or password.')
            return redirect('backendlogin')

    return render(request, 'backend/dashboard-login.html')



def backend_dashboard(request):
    # current_user = request.user
    # supr= current_user.is_superuser != True
    # print(supr)
        
        
    if 'tokenadmin' not in request.session:
        return redirect('backendlogin')  
    
    # if request.user.is_superuser == True:

    users = User.objects.all()#[1:]
    current_user = request.user 
    user_name = current_user.username 
    context = {
        'users':users,
        'user_name':user_name,
    }
     
    return render(request, 'backend/dashboard.html',context)


def viewdetail_dashboard(request,id):
    if 'tokenadmin' not in request.session:
        return redirect('backend-login')
    if request.method == 'POST':
        view_detail = Birthdata.objects.all()
        print (view_detail)
        
        
        
    current_user = request.user 
    user_name = current_user.username
    view_detail = Birthdata.objects.filter(Q(user_id=id))
    print (view_detail)
    
    context = {
        "view_detail": view_detail,
        'user_name':user_name,
        'user_id':id,
    }
    return render(request, 'backend/viewbirthdata.html',context)

# delete detail views...

def deletedetail_dashboard(request,id):
    try:
        # User.objects.filter(id=id).delete()
        users = User.objects.filter(id=id)
        users.delete()
        messages.success(request, "The user is deleted")  
        return redirect('backend')          

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        # return render(request, 'backend/dashboard.html')

    context = {
        'users':users,
    }
    
    return render(request, 'backend/dashboard.html',context)

# View birth details...

def view_birth_details(request,id):
    if 'tokenadmin' not in request.session:
        return redirect('backend-login')
    current_user = request.user 
    user_name = current_user.username
    view_detail = Birthdata.objects.get(id=id)
    context = {
        "view_detail": view_detail,
        'user_name':user_name,
    }
    return render(request, 'backend/view-birth-details.html',context)

# Send mail with single birth...

def send_mail_single_birth(request,id):
    if 'tokenadmin' not in request.session:
        return redirect('backend-login')
    current_user = request.user 
    user_name = current_user.username
   
    view_detail = Birthdata.objects.get(id=id)
    user_detail = User.objects.get(id=view_detail.user_id) 
    
    context = {
        "view_detail": view_detail,
        'user_name':user_name,
    }
    s = datetime.strptime(view_detail.time_of_birth, "%H:%M")
    birth_time = s.strftime("%I:%M %p")    
    # configure your email address
    # step1:
    email_user = 'uttam.synetalsolutions@gmail.com'
    email_password = 'aexqwqejdextcaer'
    email_send = 'uttam.synetalsolutions@gmail.com'

    # step2:
    # https://myaccount.google.com/lesssecureapps
    # Allow less secure apps: ON (remember you must be on for sending email)

    subject = 'Contact Information'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    msg.attach(MIMEText('<html><body><p>Hi Admin, <br> PFA</p><h4>Thanks & Regards</h4><p>'+user_detail.  username+'</p></body></html>', 'html', 'utf-8'))

    filename = 'text.cin'
    with open(filename, "w+") as file1:
        L = ["NM1:", view_detail.full_name, '\n', "DT1:", str(view_detail.date_of_birth), '\n', "TM1:", str(birth_time), '\n', "PL1:", view_detail.birth_city_sate,
                '\n', "LONG1: ", view_detail.longitude, '\n', "LAT1: ", view_detail.lattitude, '\n', "TDATE:", str(view_detail.transits_chart_date), '\n', "DONE:"]
        file1.writelines(L)
        file1.close()
    with open(filename, "r") as f:
        part = MIMEApplication(f.read(), Name=basename(filename))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(
            basename(filename))
    msg.attach(part)
 
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
    messages.success(request, 'Email send sucessfully')
    if os.path.isfile(filename):
            os.remove(filename)
    return redirect('/backend-login/backend/viewdetail/'+str(view_detail.user_id))

# Send mail with Multiple birth...

def send_mail_multiple_birth(request,user_id):
    if 'tokenadmin' not in request.session:
        return redirect('backend-login')
    user_detail = User.objects.get(id=user_id)
    if request.method == 'POST':
        check_user_id = request.POST.getlist('check_user_id[]')
        for i in check_user_id:
            view_detail = Birthdata.objects.get(id=i) 
            s = datetime.strptime(view_detail.time_of_birth, "%H:%M")
            birth_time = s.strftime("%I:%M %p")    
            # configure your email address
            filename = 'text.cin'
            with open(filename, "a+") as file1:
                # file1 = open(filename, "a+")
                L = ["NM1:", view_detail.full_name, '\n', "DT1:", str(view_detail.date_of_birth), '\n', "TM1:", str(birth_time), '\n', "PL1:", view_detail.birth_city_sate,
                        '\n', "LONG1: ", view_detail.longitude, '\n', "LAT1: ", view_detail.lattitude, '\n', "TDATE:", str(view_detail.transits_chart_date), '\n', "DONE:","",'\n\r']
                file1.writelines(L)
                file1.close()
                # step1:
        email_user = 'uttam.synetalsolutions@gmail.com'
        email_password = 'aexqwqejdextcaer'
        email_send = 'uttam.synetalsolutions@gmail.com'

        # step2:
        # https://myaccount.google.com/lesssecureapps
        # Allow less secure apps: ON (remember you must be on for sending email)

        subject = 'Contact Information'
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        msg.attach(MIMEText('<html><body><p>Hi Admin, <br> PFA</p><h4>Thanks & Regards</h4><p>'+user_detail.username+'</p></body></html>', 'html', 'utf-8'))
        filename = 'text.cin'
        with open(filename, "r") as f:
            part = MIMEApplication(f.read(), Name=basename(filename))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(
                basename(filename))
        msg.attach(part)

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_send, text)
        server.quit()
        messages.success(request, 'Email send sucessfully')
        if os.path.isfile(filename):
            os.remove(filename)
        return redirect('/backend-login/backend/viewdetail/'+str(user_id))
        

# Backend dashboard logout...
def backend_dashboard_logout(request):
    del request.session['tokenadmin']
    messages.success(request, 'Logout successfully.')
            
    return redirect('backendlogin')

# Backend change password...
def backend_dashboard_changpassword(request):
    if 'tokenadmin' not in request.session:
        return redirect('backend-login')
    current_user = request.user 
    user_name = current_user.username
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password changed sucessfully')
                return redirect('backendlogin')
        else:
            fm = SetPasswordForm(user=request.user)
    return render (request, 'backend/backend-change-password.html',{'form': fm,'user_name': user_name,})
