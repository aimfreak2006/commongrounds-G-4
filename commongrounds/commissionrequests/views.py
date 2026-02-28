from django.shortcuts import render
from .models import Commission

def list_view(request):
    commissions = Commission.objects.all()
    dictionary = {"commissions" : commissions}
    return render(request, 'comissionsrequests/commission_list.html', dictionary)

def detail_view(request, pk):
    commission = Commission.objects.get(pk=pk)
    dictionary = {"commission" : commission}
    return render(request, 'comissionsrequest/commission_detail.html', dictionary)
