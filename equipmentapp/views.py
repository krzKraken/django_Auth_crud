from django.shortcuts import render, redirect

# Library to create user in django
from django.contrib.auth.models import User

# Library to create form in django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

#  Library to create session token
from django.contrib.auth import login, logout, authenticate

# Import the form created
from .forms import TaskForm

# import the task model
from .models import Task

# Create your views here.

# Home Page
def home(request):
    return render(request, "home.html")


# Signup Page
def signup(request):
    if request.method == "GET":
        print("Enviando form")
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        print("Recibiendo form")
        if request.POST["password1"] == request.POST["password2"]:
            # register USer
            print("Passwords no counciden")
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exist"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Password does not match"},
        )


def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks.html", {"tasks": tasks})


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")


def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        # print(request.POST)
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Please provide valid data"},
            )


# # Signup form from django
# def signupform(request):
#     return render(request, "signup.html", {"form": UserCreationForm})


# # Sign_up Form from django con token csrf
# def sign_up_form(request):
#     return render(
#         request,
#         "sign_up.html",
#         {
#             "form": UserCreationForm,
#         },
#     )


# # httpResponse
# def helloword(request):
#     return HttpResponse("<h1>Hello word</h1>")


# # Render a .html file
# def htmlform(request):
#     return render(request=request, template_name="form.html")


# # Sending arguments to html file
# def sendingargument(request):
#     name = "Kraken"
#     lastname = "Insane"
#     return render(
#         request=request,
#         template_name="examples.html",
#         context={
#             "myname": name,
#             "mylastname": lastname,
#         },
#     )
