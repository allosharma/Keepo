from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *
from .fetch_youtube_transcript import *
from .youtubeAPIFetch import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def homePage(request):
    if request.method == "POST":
        data = request.POST
        youtube_link = data.get('ytLink') # It returns youtube link
        checkbox_options = data.getlist('options') # It returns list of selected checkbox elements.
        yoututbe_id = extract_video_id(youtube_link)
        youtube_video_transcription = get_transcription(yoututbe_id)
        filename = "core/transcript/{}.txt".format(yoututbe_id)

        with open (filename, "w") as f:
            f.write(youtube_video_transcription)

        print(yoututbe_id, checkbox_options)

        request.session['value'] = yoututbe_id # pass value from this view to another

        return redirect('/description/')


    user_params = ['Conclusion', 'Quiz', 'Reason']
    context = {'user_params': user_params}
    return render(request, 'index.html', context)

def loginPage(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('homePage')


    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('/login/')

def registerPage(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        # print(first_name, last_name, username, password)

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, "User exists already")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully.")

        return redirect('/register/')


    return render(request, 'register.html')


@login_required(login_url="/login/")
def videoDescription(request):
    value = request.session.get('value', None)
    api_response = fetchYoutubeData(value)
    # Extract description from the JSON response if it's available
    # description = (
    #     api_response['items'][0]['snippet']['description']
    #     if 'items' in api_response and api_response['items']
    #     else "Description not available."
    # )
    description = api_response['items'][0]['snippet']['description']
    title = api_response['items'][0]['snippet']['title']
    context = {'value': value, 'title':title, 'description':description}
    # print('hello world:', description)
    return render(request, 'videoDescription.html', context)