from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.contrib import messages

def home(request):
    return render(request,'home.html')

def signuppage(request):
    if request. method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        passsword1=request.POST.get('password1')
        passsword2=request.POST.get('password2')
        if passsword1!=passsword2:
            messages.error(request,"Passwords are not same!")
            return redirect('signup')
        try:
            if User.objects.get(username=username):
                messages.info(request,"Username is taken.")
                return redirect('signup')
        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email is taken.")
                return redirect('signup')
        except:
            pass
        my_user=User.objects.create_user(username,email,passsword1)
        my_user.save()
        return redirect('room')
    return render(request,'signup.html')

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('room')
        else:
            messages.error(request,'username or password is incorrect!')
            # return HttpResponse("username or password is incorrect")
    return render (request,'login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')    
def roomview(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room, username=username)

    return render(request, 'index.html')

@login_required(login_url='login')
def MessageView(request, room_name, username):

    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages= Message.objects.filter(room=get_room)
    
    context = {
        "messages": get_messages,
        "user": username
    }
    return render(request, 'message.html', context)
