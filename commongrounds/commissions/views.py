from django.shortcuts import render
from .models import Commission, CommissionType, Job
from .forms import CommissionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def list_view(request):
    created_commissions = Commission.objects.filter(maker=request.user)
    other_commissions = Commission.objects.exclude(maker=request.user)
    dictionary = {
        "created_commissions": created_commissions,
        "all_commissions": other_commissions,
    }
    if (request.method == "POST"):
        commission_form = CommissionForm(request.POST)
        if (commission_form.is_valid):
            commission = commission_form.save(commit=False)
            commission.maker = request.user
            commission.save()
            return redirect('/requests/')
    return render(request, 'commissions/commission_list.html', dictionary)

def detail_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    jobs = Job.objects.filter(commission=commission)
    dictionary = {
        "commission": commission,
        "jobs": jobs
    }
    return render(request, 'commissions/commission_detail.html', dictionary)

def add_view(request):
    commission_form = CommissionForm()
    dictionary = {
        "form" : commission_form
    }
    return render(request, 'commissions/commission_add.html', dictionary)

def edit_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    dictionary = {"commission": commission}
    return render(request, 'commissions/commission_edit')
