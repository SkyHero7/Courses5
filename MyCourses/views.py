from django.shortcuts import render, get_object_or_404, redirect
from .models import Mailing
from .forms import MailingForm
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    return render(request, 'index.html')
def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'MyCourses/mailing_list.html', {'mailings': mailings})

def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, owner=request.User)
    return render(request, 'MyCourses/mailing_detail.html', {'mailing': mailing})

def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save()
            return redirect('mailing_detail', pk=mailing.pk)
    else:
        form = MailingForm()
    return render(request, 'MyCourses/mailing_form.html', {'form': form})

def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            mailing = form.save()
            return redirect('mailing_detail', pk=mailing.pk)
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'MyCourses/mailing_form.html', {'form': form})

def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing_list')
    return render(request, 'MyCourses/mailing_confirm_delete.html', {'mailing': mailing})

def edit_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing_list')
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'MyCourses/mailing_edit.html', {'form': form})

