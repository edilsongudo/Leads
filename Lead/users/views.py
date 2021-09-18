from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import Profile


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


@login_required
def profileimage(request):
    profile = Profile.objects.get(user=request.user)
    print('REQUEST RECEIVED')
    profile.image = request.FILES.get('cropped')
    profile.save()
    return JsonResponse({'success': 'success'})
