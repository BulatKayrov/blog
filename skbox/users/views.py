from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib import auth
from .forms import SignUpForm, SignInForm, ProfileForm
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .models import User
from .tasks import verified_accounts


def verify(request, code):
    user = User.objects.get(username=request.user.username)
    if user.code_verified == code:
        user.is_verified = True
        user.save()
        return render(request, template_name='users/verify.html')
    return render(request, template_name='users/verify_error.html')


@login_required(login_url='users:login')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = ProfileForm(instance=request.user)

    posts = Post.objects.filter(author=request.user)

    context = {
        'form': form,
        'posts': posts
    }

    return render(request=request, template_name='users/profile.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('blog:index'))

    else:
        form = SignInForm()

    context = {'form': form}
    return render(request=request, template_name='users/login.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect(reverse('users:login'))


def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            verified_accounts.delay(email=user.email, uuid_code=user.code_verified)
            return redirect(reverse('blog:index'))

    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request=request, template_name='users/register.html', context=context)
