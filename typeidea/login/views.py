from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView,DetailView
from .models import MyUser
from .forms import UserForm,RegisterForm
import hashlib

def hash_code(s, salt='my_blog'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class LoginView(TemplateView):
    template_name = 'login/login.html'

    def post(self, request, *args, **kwargs):
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            if username.strip() and password:
                try:
                    user = MyUser.objects.get(name=username)
                except:
                    message = '用户不存在'
                    return render(request, 'login/login.html', locals())

                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/')
                else:
                    message = '请输入正确的用户名和密码'
                    return render(request, 'login/login.html', locals())
            else:
                message = '请输入正确的用户名和密码'
                return render(request, 'login/login.html', locals())
        else:
            print('form 无效')
            return render(request, 'login/login.html', locals())

    def get(self, request, *args, **kwargs):
        print('gegetget')
        context = {'login_form': UserForm()}
        return self.render_to_response(context)





class RegisterView(TemplateView):
    template_name = 'login/register.html'

    def post(self, request, *args, **kwargs):
        form_register = RegisterForm(request.POST)
        if form_register.is_valid():
            data = form_register.cleaned_data
            username = data.get('username')
            password = data.get('password')
            password2 = data.get('password2')
            email = data.get('email')
            sex = data.get('sex')
            if password != password2:
                message = '两次输入的密码不相同！'
                return render(request, 'login/register.html', locals())
            else:
                same_user = MyUser.objects.filter(name=username)
                same_email = MyUser.objects.filter(email=email)
                if same_user:
                    message = '用户名已存在'
                    return render(request, 'login/register.html', locals())
                elif same_email:
                    message = '邮箱已存在'
                    return render(request, 'login/register.html', context={'form_register': form_register,
                                                                           'message':message,})
                else:
                    user = MyUser()
                    user.password = hash_code(password)
                    user.email = email
                    user.sex = sex
                    user.name = username
                    user.save()
                    return redirect('/login')
        else:
            return render(request, 'login/register.html', locals())
        # try:
        #     user = User.objects.get(name=username)
        #     alert_message = "用户已存在"
        # except:


    def get(self, request, *args, **kwargs):
        context = {'form_register': RegisterForm()}
        return self.render_to_response(context)


class LogoutView(TemplateView):
    template_name = 'login/logout.html'