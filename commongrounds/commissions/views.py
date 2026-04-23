from django.shortcuts import render
from .models import Commission, CommissionType
from .forms import CommissionForm


def list_view(request):
    commission_requests = Commission.objects.all()
    dictionary = {
        "requests": commission_requests,
    }
    return render(request, 'commissions/commission_list.html', dictionary)


def detail_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    dictionary = {
        "commission": commission
    }
    return render(request, 'commissions/commission_detail.html', dictionary)

def add_view(request):
    commission_form = CommissionForm()
    dictionary = {
        "form" : commission_form
    }
    return render(request, 'commissions/commission_add.html', dictionary)

def edit_view(request, pk):
    pass
