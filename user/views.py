from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():#Burada yazdığımız clean methodu çalışıyor.
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            newUser = User(username=username)
            newUser.set_password(password)#parolayı şifreledik.
            newUser.save() #Kullanıcıyı veritabanına kaydettik.
            login(request,newUser)#Kaydettikten sonra otomatik giriş yaptık.
            messages.success(request,"Başarıyla Kayıt Oldunuz...")
            return redirect("index")
        context = {
            "form":form
        }
        return render(request,"register.html",context)
    else:
        form = RegisterForm()
        context = {
            "form":form
        }
        return render(request,"register.html",context)
    

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request,"Kullanıcı adı veya parola hatalı")
            return render(request,"login.html",context)
        
        messages.success(request,"Başarıyla giriş yaptınız...")
        login(request,user)
        return redirect("index")
    else:
        return render(request,"login.html",context)
    

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız...")
    return redirect("index")

