from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TravelAgencyCVForm
from .models import TravelAgencyCV, Language

@login_required
def create_or_update_cv(request):
    try:
        cv = request.user.cv
    except TravelAgencyCV.DoesNotExist:
        cv = None

    if request.method == 'POST':
        form = TravelAgencyCVForm(request.POST, request.FILES, instance=cv)
        if form.is_valid():
            cv_instance = form.save(commit=False)
            cv_instance.user = request.user
            cv_instance.save()
            form.save_m2m()

            # Handle new languages as before...

            messages.success(request, "Your CV has been saved successfully.")
            return redirect('accounts:guest_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial = {}
        if cv:
            initial['languages'] = cv.languages.all()
        form = TravelAgencyCVForm(instance=cv, initial=initial)

    return render(request, 'create_cv_guest.html', {'form': form})
