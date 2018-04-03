from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_log:index'))
def register(request):
    if request.method !='POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save() #注册用户到数据库，返回这个用户数据，返回的密码已经是加密的了
            #创建一个用户信息变量用于login(),password不使用new_user.password 是因为加密处理
            authenticate_user = authenticate(username=new_user.username,password = request.POST['password1'])
            login(request,authenticate_user)
            return HttpResponseRedirect(reverse('learning_log:index'))
    return render(request,'users/register.html',locals())