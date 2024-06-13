from django.shortcuts import render, redirect
from .forms import MedicineForm
from .models import Medicine
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form =MedicineForm()
    return render(request, 'add.html', {'form': form})

@login_required(login_url='/login/')
def medicine_list(request):
    medicine_list=Medicine.objects.all()
    return render(request,'medicine_list.html',{'medicine_list':medicine_list})

def update_medicine(request, pk):
    medicine= Medicine.objects.get(pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST,instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form =MedicineForm(instance=medicine)           
    return render(request, 'update.html', {'form': form})


def delete_medicine(request,pk):
    medicine=Medicine.objects.get(pk=pk)  
    if request.method == 'POST':
        medicine.delete()
        return redirect('home')
    
    return render(request,'delete.html',{'medicine':medicine})

from django.shortcuts import render, redirect
from .models import Medicine

def search_medicine(request):
    query = request.GET.get('q')
    if query:
        medicines = Medicine.objects.filter(name__icontains=query)
        return render(request, 'search_results.html', {'medicines': medicines})
    else:
        return redirect('medicine_list')
    
