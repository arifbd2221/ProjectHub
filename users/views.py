from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib import messages, sessions
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib.auth import login, authenticate
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Message
from itertools import chain


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('users/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'Your account has been created! You are now able to log in')
            # return redirect('login')
            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def messageTo(request, id):
    senderMsg = Message.objects.filter(sender=request.user.id).filter(recipient=id)
    recieverMsg = Message.objects.filter(recipient=request.user.id).filter(sender=id)
    allmsg = list(chain(senderMsg, recieverMsg))

    try:
        id = recieverMsg[0].id
    except IndexError as ie:
        id = 0

    return render(request, 'users/chatting.html', {'allmsg': allmsg, 'recp': id,})


def saveMsg(request, recp):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        user = get_object_or_404(User, id=recp)
        Message.objects.create(content=msg, sender=request.user, recipient=user)

    return redirect('chat', id=recp)
