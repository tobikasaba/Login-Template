from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # grabbing the user form and saving it to the database
            user = user_form.save()
            # hashing the password i.e. setting the password
            user.set_password(user.password)
            # saving the user record with its password
            user.save()

            # commit = False prevents saving the data in the database to prevent conflicts and errors
            profile = profile_form.save(commit=False)
            # defines a one-to-one relationship with user
            profile.user = user

            """
            the UserProfileInfo model has a profile_pic field
            This line checks whether the form submission includes a file with the name "profile_pic"
            This is the method used with all files
            """
            if 'profile_pic' in request.FILES:
                """
                if a file was uploaded (i.e., the "profile_pic" key exists in request.FILES), this line assigns the
                uploaded file to the profile_pic field of the profile model instance (which is an instance of the UserProfileInfo model).
                profile_pic is a field defined in the UserProfileInfo model using models.ImageField to handle image files.
                """
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


# login_required ensures the user has to be logged in
@login_required
def user_logout(request):
    # logouts the user
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    # if the user returns data
    if request.method == 'POST':
        print("yeah")
        # get the username and password the user put into the form
        # these are gotten directly from login.html where the labels in were named username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # redirect the user if login is successful to the index page
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is not active.')
        else:
            print("Someone tried to login and failed")
            print(f"Username: {username} and password: {password}")
            return HttpResponse('Invalid Login details supplied.')
    else:
        return render(request, 'basic_app/login.html', {})
