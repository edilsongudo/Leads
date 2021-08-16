from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileImageForm
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import Profile

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Your Account has been created. You are now able to login.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        i_form = ProfileImageForm(request.POST,
                                  request.FILES,
                                  instance=request.user.profile)
        if request.is_ajax():
            profile = Profile.objects.get(user=request.user)
            profile.image = request.FILES.get('cropped')
            profile.save()

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        i_form = ProfileImageForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'i_form': i_form
    }

    return render(request, 'users/profile.html', context)
