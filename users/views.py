from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
import requests
import json


# Create your views here.
def home(request):
    return render(request, 'login.html')

def tickets(request):
    return render(request, 'tickets.html')

def handleSignUp(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        number=request.POST['number']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
            
        #error handling

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('home')

            #creating user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.number=number
        myuser.pass2=pass2
        myuser.save()
        messages.success(request, "Your regestred now ")
        return redirect('home')
             
    

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        password=request.POST['password']
        user=authenticate(username= loginusername, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")
        


def handleLogout(request): 
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')



def sendTickets(request):
    if request.method == 'POST':
        Department = request.POST['Department']
        Category = request.POST['Category']
        Subject =request.POST['Subject']
        email =request.POST['email']
        Descripation = request.POST['descripation']
        Priority = request.POST['Priority']
    
    print(Department,Category,Subject,email,Priority,Descripation)
    
    url = "https://desk.zoho.in/api/v1/tickets"
    headers = {'orgId':'60014678075','Authorization':'Zoho-oauthtoken 1000.bcf2659490379cb00bc681aed305d554.0203a850513ff536effa30b725b09757'}
    payload = {"departmentId" : "75347000000010772","contactId" : "75347000000122029"}
    payload.update({'subject' : Subject})
    payload.update({'description' : Descripation})
    payload.update({"email" : email})
    payload.update({"priority" : Priority})

    print(payload)
    jsonData =json.dumps(payload)
    response = requests.post(url, headers=headers, data=jsonData)
    print(response.text)



    return redirect('GetTickets')

def GetTickets(request):
    url = "https://desk.zoho.in/api/v1/tickets"
    headers = {'orgId':'60014678075','Authorization':'Zoho-oauthtoken 1000.bcf2659490379cb00bc681aed305d554.0203a850513ff536effa30b725b09757'}
    response = requests.get(url, headers=headers)
    c = json.loads(response.text)
    tickets = c['data']
    print(c['data'])
    for i in c['data']:
        print(i['subject'])
    return render(request, 'list.html', {'tickets':tickets})
    



