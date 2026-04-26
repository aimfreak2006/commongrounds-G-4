from django.shortcuts import render
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def get_applied_commissions(request):
    jobs = []
    applied_commissions = dict()
    job_forms_answered = JobApplication.objects.filter(applicant=request.user.profile)
    
    for job_form_answered in job_forms_answered:
        jobs.append(job_form_answered.job)

    for job in jobs:
        applied_commissions[job.commission] = job.commission

    return applied_commissions

def get_remaining_commissions(request, applied_commissions):
    commissions_without_created = Commission.objects.exclude(maker=request.user.profile)
    remaining_commissions = []
    for commission in commissions_without_created:
        if (commission not in applied_commissions):
            remaining_commissions.append(commission)

    return remaining_commissions

def get_jobs_current_manpowers(commission):
    ACCEPTED = '1A'
    jobs = Job.objects.filter(commission=commission)
    current_manpowers = dict()
    for job in jobs:
        accepted_applicants_count = JobApplication.objects.filter(job=job, status=ACCEPTED).count()
        current_manpowers[job] = job.manpower_required - accepted_applicants_count

    return current_manpowers

@login_required
def list_view(request):
    created_commissions = Commission.objects.filter(maker=request.user.profile)
    applied_commissions = get_applied_commissions(request)
    other_commissions = get_remaining_commissions(request, applied_commissions)

    JobFormSet = inlineformset_factory(
        Commission, 
        Job, 
        form=JobForm, 
        extra=3, 
        can_delete=True
    )
    dictionary = {
        "created_commissions": created_commissions,
        "applied_commissions": applied_commissions,
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

def is_applied(request, jobs):
    for job in jobs:
        if (job.application.filter(applicant=request.user.profile)):
            print(job.application.filter(applicant=request.user.profile))
            return True
    return False

@login_required
def detail_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    jobs = get_jobs_current_manpowers(commission)
    is_user_applied = is_applied(request, jobs)

    dictionary = {
        "commission": commission,
        "jobs": jobs,
        "is_applied" : is_user_applied,
    }


    if (request.method == "POST"):
        commission_form = CommissionForm(request.POST, instance=commission)
        if (commission_form.is_valid()):
            commission_form.save()

        if ("apply_to_job" in request.POST):
            job_id = request.POST.get("job_id")
            job = Job.objects.get(pk=job_id)
            
            JobApplication.objects.create(
                job=job,
                applicant=request.user.profile
            )
            return redirect('commissions:detail_view', pk=pk)
    return render(request, 'commissions/commission_detail.html', dictionary)

@login_required
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

@login_required
def edit_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    commission_form = CommissionForm(request.POST, instance=commission)
    dictionary = {
        "commission": commission,
        "form": commission_form
    }
    return render(request, 'commissions/commission_edit.html', dictionary)
