from django.shortcuts import render
from django.forms import inlineformset_factory
from .models import Commission, Job
from .forms import CommissionForm, JobForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def list_view(request):
    created_commissions = Commission.objects.filter(maker=request.user.profile)
    other_commissions = Commission.objects.exclude(maker=request.user.profile)
    JobFormSet = inlineformset_factory(
        Commission, 
        Job, 
        form=JobForm, 
        extra=3, 
        can_delete=True
    )
    dictionary = {
        "created_commissions": created_commissions,
        "other_commissions": other_commissions
    }
    if (request.method == "POST"):
        commission_form = CommissionForm(request.POST)
        job_forms = JobFormSet(request.POST)
        if (commission_form.is_valid() and job_forms.is_valid()):
            commission = commission_form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()
            job_forms.instance = commission 
            job_forms.save()
            return redirect('/commissions/requests/')
    return render(request, 'commissions/commission_list.html', dictionary)

def detail_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    jobs = Job.objects.filter(commission=commission)
    dictionary = {
        "commission": commission,
        "jobs": jobs
    }
    if (request.method == "POST"):
        commission_form = CommissionForm(request.POST, instance=commission)
        if (commission_form.is_valid()):
            commission_form.save()
    return render(request, 'commissions/commission_detail.html', dictionary)

def add_view(request):
    commission_form = CommissionForm()
    JobFormSet = inlineformset_factory(
        Commission, 
        Job, 
        form=JobForm, 
        extra=3, 
        can_delete=True
    )
    job_forms = JobFormSet()
    dictionary = {
        "commission_form": commission_form,
        "job_forms": job_forms
    }
    return render(request, 'commissions/commission_add.html', dictionary)

def edit_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    commission_form = CommissionForm(request.POST, instance=commission)
    dictionary = {
        "commission": commission,
        "form": commission_form
    }
    return render(request, 'commissions/commission_edit.html', dictionary)
