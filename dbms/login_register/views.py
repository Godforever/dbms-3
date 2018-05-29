from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django import forms
from . import mysql
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext

class RegisterUserForm(forms.Form):
    username = forms.CharField(label="username", max_length=32)
    nickname = forms.CharField(label="nickname", max_length=32)
    name = forms.CharField(label="name", max_length=20)
    sex = forms.CharField(label="sex")
    birthdate = forms.CharField(label="birthdate")
    email = forms.CharField(label="email")
    address = forms.CharField(label="address",max_length=45)
    password = forms.CharField(label="password", widget=forms.PasswordInput())

class LoginUserForm(forms.Form):
    username = forms.CharField(label="username", max_length=32)
    password = forms.CharField(label="password", widget=forms.PasswordInput())


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        nickname = request.POST['nickname']
        name = request.POST['name']
        sex = request.POST['sex']
        birthdate = request.POST['birthdate']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']
        message = mysql.register(username, nickname, name, sex, birthdate, email, address, password)
        if message != 2 :
            return render_to_response('share.html', {'message': message, 'username': username})
        else:
            return render_to_response('login.html', {'username': username})

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        luf = LoginUserForm(request.POST)
        if luf.is_valid():
            username = luf.cleaned_data['username']
            password = luf.cleaned_data['password']
            message = mysql.login(username, password)
            if message == 3:
                response = HttpResponseRedirect('/index/')
                response.set_cookie('username', username, 3600)
                return response
            else:
                return HttpResponseRedirect('/login')
    else:
        luf = LoginUserForm()
    return render(request, 'login.html',{'luf':luf})

def index(request):
    if request.COOKIES.get('username', ''):
        username = request.COOKIES.get('username', '')
    else:
        username = request.GET['username']
    return render_to_response('index.html',{'username':username})

def home(request):
    return render_to_response('home.html')

def logout(request):
    response = HttpResponse('logout!!!')
    # 清除cookie里保存的username
    response.delete_cookie('username')
    return response

def share(request):
    if request.method == 'POST':
        uf = LoginUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            return render_to_response('share.html',{'username':username})
    else:
        uf = LoginUserForm()
    return render_to_response('share.html',{'uf':uf})


def fix_personal_information(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    if request.method == 'POST':
        username = request.POST['username']
        nickname = request.POST['nickname']
        name = request.POST['name']
        sex = request.POST['sex']
        birthdate = request.POST['birthdate']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']
        message = mysql.update_personal_information(username, nickname, name, sex, birthdate, email, address,password)
        if message == 2:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('username', username, 3600)
            return response
        else:
            return HttpResponseRedirect('/fix_p?username='+username)
    return render(request, 'fix_p.html',{'username':username})

def fix_educational_information(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    if request.method == 'POST':
        username = request.POST['username']
        level = request.POST['level']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        school_name = request.POST['school_name']
        degree = request.POST['degree']
        message = mysql.insert_update_education_experience(username, level,start_date,end_date,school_name,degree)
        if message == 1:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('username', username, 3600)
            return response
        else:
            return HttpResponseRedirect('/fix_e?username'+username)
    return render(request, 'fix_e.html', {'username': username})


def fix_work_information(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    if request.method == 'POST':
        username = request.POST['username']
        employer = request.POST['employer']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        position = request.POST['position']
        message = mysql.insert_update_work_experience(username, employer,start_date,end_date,position)
        if message == 1:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('username', username, 3600)
            return response
        else:
            return HttpResponseRedirect('/fix_w')
    return render(request, 'fix_w.html', {'username': username})

def show_personal_information(request):
    username = request.GET['username']
    results, message = mysql.load_information(username)
    return render(request, 'show_p.html', {'pi': results[0],'ee':results[1], 'we':results[2], 'message': message, 'username': username})


def show_logs(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    results, message = mysql.load_logs(username)
    return render(request, 'show_logs.html',{'results':results,'message':message, 'username':username})

def add_log(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    if 'log' in request.POST:
        log = request.POST['log']
        message = mysql.deliver_log(username, log)
        if message == 1:
            return HttpResponseRedirect('/show_logs?username='+username)
    return render(request, 'add_log.html',{'username':username})

def add_friend(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    if 'friend_username' in request.POST:
        friend_username = request.POST['friend_username']
        group = request.POST['group']
        message = mysql.add_friend(username, friend_username, group)
        if message == 2:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('username', username, 3600)
            return response
    return render(request, 'add_friend.html', {'username': username})

def show_friends(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    results, message = mysql.load_friends(username)
    group = []
    for result in results:
        group.append(result['group'])
    group = list(set(group))
    new_result = [[] for i in range(len(group))]
    for i in range(len(group)):
        for result in results:
            if result['group'] == group[i]:
                new_result[i].append(result)
    results = [(a,b) for a,b in zip(group, new_result)]
    return render(request, 'show_friends.html', {'results': results, 'message': message, 'username':username})


def add_reply(request):
    username = request.POST['username']
    log_id = request.POST['log_id']
    to_username = request.POST['to_username']
    reply_content = request.POST['reply_content']
    mysql.add_reply(username, log_id,reply_content, to_username)
    results, message = mysql.load_logs(username)
    return render(request, 'show_logs.html', {'results': results, 'message': message, 'username': username})

def share_log(request):
    username = request.POST['username']
    log_id = request.POST['log_id']
    mysql.share_log(username, log_id)
    results, message = mysql.load_logs(username)
    return render(request, 'show_logs.html', {'results': results, 'message': message, 'username': username})

def search_friend(request):
    if request.GET['username']:
        username = request.GET['username']
    else:
        username = request.POST['username']
    if 'friend_username' in request.POST:
        friend_username = request.POST['friend_username']
        results, message = mysql.load_information(friend_username)
        return render(request, 'show_p.html',
                      {'pi': results[0], 'ee': results[1], 'we': results[2], 'message': message,
                       'username': username})

    return render(request, 'search_friend.html', {'username': username})

def delete_friend(request):
    username = request.POST['username']
    friend_username = request.POST['friend_username']
    mysql.delete_friend(username, friend_username)
    results, message = mysql.load_friends(username)
    return HttpResponseRedirect('show_friends?username=' + username)


def delete_group(request):
    username = request.POST['username']
    group_name = request.POST['group']
    mysql.delete_group(username, group_name)
    return HttpResponseRedirect('show_friends?username='+username)

def update_group(request):
    username = request.POST['username']
    group = request.POST['group']
    if 'new_group' in request.POST:
        new_group = request.POST['new_group']
        mysql.update_group(username, group, new_group)
        return HttpResponseRedirect('show_friends?username=' + username)
    else:
        return render(request, 'fix_g.html', {'username': username, 'group':group})
