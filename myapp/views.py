from django.shortcuts import redirect, render
from .forms import usersignupform,notesdataform,contactdataform
from .models import usersignup
from django.contrib.auth import logout
from django.core.mail import send_mail
from BatchProject import settings
import requests
import json
import random

# Create your views here.

def newuserRegi(request):
    signupform=usersignupform(request.POST)
    if signupform.is_valid():
        signupform.save()
        print("Signup Successfully!")
    else:
        print(signupform.errors)

def userLogin(request):
    unm=request.POST["username"]
    pas=request.POST["password"]

    userID=usersignup.objects.get(username=unm)
    print("UserID:",userID.id)
    user=usersignup.objects.filter(username=unm,password=pas)
    if user:
        print("Login Successfully!")
        request.session["user"]=unm
        request.session["userid"]=userID.id
    else:
         print("Error..Login faild!")

def index(request):
    user=request.session.get('user')
    if request.method=='POST':
        if request.POST.get("signup")=="signup":
            newuserRegi(request)

            # Send confirmation mail
            sub='Welcome!'
            msg='Hello User\nYour account has been create with us!\nEnjoy our services!\n\nThanks & Regards\nTOPS Technologies Pvt. Ltd\n+91 9724799469 | sanket.tops@gmail.com'   
            from_mail=settings.EMAIL_HOST_USER
            #to_email=['sanketbarot74@gmail.com','jugalgajjar11@gmail.com','himalaygoswami43@gmail.com','jayrajmori111@gmail.com','janvijobanputra08@gmail.com']
            to_mail=[request.POST['username']]

            send_mail(sub,msg,from_mail,to_mail)
            return redirect('notes')
        elif request.POST.get("login")=="login":
            userLogin(request)

            # Send SMS

            otp=random.randint(1111,9999)    
            # mention url
            url = "https://www.fast2sms.com/dev/bulk"
            # create a dictionary
            my_data = {
                # Your default Sender ID
                'sender_id': 'FSTSMS',
                
                # Put your message here!
                'message': f'Your account has been login!\nYour one time password is {otp}',
                
                'language': 'english',
                'route': 'p',
                
                # You can send sms to multiple numbers
                # separated by comma.
                'numbers': '8347199144,7984220921,8160746985,7405570575,9574260801'	
            }

            # create a dictionary
            headers = {
                'authorization': 'guiISqOUov6f3RFEraCDW1cKHYAG8P5XQtbhkTp4dMel9wmxN7K9PzIUDapAWBOmvfkN8so0q4HFLEiJ',
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache"
            }

            # make a post request
            response = requests.request("POST",
                                        url,
                                        data = my_data,
                                        headers = headers)
            
            #returned_msg = json.loads(response.text)
            #returned_msg = json.load(response.text)
            # print the send message
            #print(returned_msg['message'])
            print("SMS Send successfully!")
            return redirect('notes')
    return render(request,'index.html',{'user':user})

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        notesUpload=notesdataform(request.POST,request.FILES)
        if notesUpload.is_valid():
            notesUpload.save()
            print("Your post has been uploaded!")
        else:
            print(notesUpload.errors)
    return render(request,'notes.html',{'user':user})

def userlogout(request):
    logout(request)
    return redirect("/")

def profile(request):
    user=request.session.get('user')
    userid=request.session.get('userid')
    id=usersignup.objects.get(id=userid)
    if request.method=='POST':
        userupdate=usersignupform(request.POST)
        if userupdate.is_valid():
            userupdate=usersignupform(request.POST,instance=id)
            userupdate.save()
            print("Your profile has been updated!")
            return redirect('/')
        else:
            print(userupdate.errors)
    return render(request,'profile.html',{'user':user, 'userid':usersignup.objects.get(id=userid)})

def about(request):
    user=request.session.get('user')
    return render(request,'about.html',{'user':user})

def contact(request):
    user=request.session.get('user')
    if request.method=='POST':
        cnform=contactdataform(request.POST)
        if cnform.is_valid():
            cnform.save()
            print("Your query has been submitted!")
        else:
            print(cnform.errors)
    return render(request,'contact.html',{'user':user})
