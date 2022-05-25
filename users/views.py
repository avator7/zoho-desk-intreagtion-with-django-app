from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
import requests
import json
from decouple import config

token = config("token")
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
    headers = {'orgId':'60014678075','Authorization':f'Zoho-oauthtoken {token}'}
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
    headers = {'orgId':'60014678075','Authorization':f'Zoho-oauthtoken {token}'}
    response = requests.get(url, headers=headers)
    c = json.loads(response.text)
    tickets = c['data']
    print(c['data'])
    for i in c['data']:
        print(i['subject'])
    return render(request, 'list.html', {'tickets':tickets})

def DeleteTickets(request, ticket_id):
    url = "https://desk.zoho.in/api/v1/tickets/moveToTrash"
    headers = {'orgId':'60014678075','Authorization':f'Zoho-oauthtoken {token}'} 
    payload = {'ticketIds':[f"{ticket_id}"]}
    jsonData =json.dumps(payload)   
    print(ticket_id)
    print(payload)
    Response = requests.post(url, headers=headers, data=jsonData)
    print(Response)
    return redirect('GetTickets')

def UpdateTickets(request, ticket_id):
    if request.method == 'POST':
        Department = request.POST['Department']
        Category = request.POST['Category']
        Subject =request.POST['Subject']
        email =request.POST['email']
        Descripation = request.POST['descripation']
        Priority = request.POST['Priority']
    
    print(Department,Category,Subject,email,Priority,Descripation)

    print(ticket_id)
    url = f"https://desk.zoho.in/api/v1/tickets/{ticket_id}"
    print(ticket_id, url)
    headers = {'orgId':'60014678075	','Authorization':f'Zoho-oauthtoken {token}'}
    payload = {'description' : "this is updated!"}
    payload.update({'subject' : Subject})
    payload.update({'description' : Descripation})
    payload.update({"email" : email})
    payload.update({"priority" : Priority})
    jsonData =json.dumps(payload)
    response = requests.patch(url, headers=headers, data=jsonData)
    print(response.text)

    return redirect('GetTickets')
    

def update(request, ticket_id):
    url = "https://desk.zoho.in/api/v1/tickets?include=contacts,assignee,departments,team,isRead"
    headers = {'orgId':'60014678075','Authorization':f'Zoho-oauthtoken {token}'}
    response = requests.get(url, headers=headers)
    c = json.loads(response.text)
    index = int(ticket_id) - 1
    tickets = c['data'][index]
    print(tickets)
    # print(c['data'])
    # for i in c['data']:
    #     print(i['subject'])
    return render(request, 'update.html', {'tickets':tickets})