from django.shortcuts import render
from .models import Commission, CommissionType


def list_view(request):
    commission_requests = Commission.objects.all()
    commission_types = CommissionType.objects.all()
    dictionary = {
        "requests": commission_requests,
        "types": commission_types,
    }
    return render(request, 'commissions/commission_list.html', dictionary)


def detail_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    dictionary = {"commission": commission}
    return render(request, 'commissions/commission_detail.html', dictionary)

def add_view(request):
    pass

def edit_view(request, pk):
    pass
