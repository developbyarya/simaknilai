from django.shortcuts import redirect, render
from api.models import Sekolah, Ringkasan
# Create your views here.
def home(request):
    passed_data = {}
    data_sekolah = Sekolah.objects.all()
    passed_data['sekolah'] = data_sekolah
    return render(request, 'home.html', passed_data) 
def ringkasan(request):
    data = {}
    if request.method =='POST':
        data['id']= request.POST['sekolah']
        data['sma'] = Sekolah.objects.get(pk=data['id']).nama
        data['sekolah'] = Sekolah.objects.all()
        return render(request, 'ringkasan.html', data) 
    return redirect('home')
