from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TravelAgencyCVForm, PassportInfoForm
from .models import TravelAgencyCV, Language, PassportInfo
from accounts.models import User

from django.shortcuts import get_object_or_404

@login_required
def create_or_update_cv(request, user_id=None):
    # If HR, can edit any guest's CV by user_id
    if request.user.role == 'hr' and user_id:
        user_to_edit = get_object_or_404(User, id=user_id, role='guest')
        try:
            cv = user_to_edit.cv
        except TravelAgencyCV.DoesNotExist:
            cv = None
    else:
        # Normal guest edits their own CV only
        try:
            cv = request.user.cv
        except TravelAgencyCV.DoesNotExist:
            cv = None

    if request.method == 'POST':
        form = TravelAgencyCVForm(request.POST, request.FILES, instance=cv)
        if form.is_valid():
            cv_instance = form.save(commit=False)
            if request.user.role == 'hr' and user_id:
                cv_instance.user = user_to_edit
            else:
                cv_instance.user = request.user
            cv_instance.save()
            form.save_m2m()

            messages.success(request, "Your CV has been saved successfully.")
            # Redirect to dashboard or detail page accordingly
            if request.user.role == 'hr' and user_id:
                return redirect('accounts:hr_guest_cv_detail', user_id=user_to_edit.id)
            else:
                return redirect('accounts:guest_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial = {}
        if cv:
            initial['languages'] = cv.languages.all()
        form = TravelAgencyCVForm(instance=cv, initial=initial)

    return render(request, 'create_cv_guest.html', {'form': form})




# Hr department

@login_required
def register_passport_info(request):
    # Only HR should access this view
    if request.user.role != 'hr':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    if request.method == 'POST':
        form = PassportInfoForm(request.POST, request.FILES)
        if form.is_valid():
            passport_info = form.save(commit=False)
            passport_info.user = request.user
            passport_info.save()
            messages.success(request, "Passport information has been successfully registered.")
            return redirect('accounts:hr_dashboard')  # Redirect to dashboard or another page
    else:
        form = PassportInfoForm()

    return render(request, 'register_passport_info.html', {'form': form})
