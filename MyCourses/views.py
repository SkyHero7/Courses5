from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mailing
from .forms import MailingForm

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'MyCourses/mailing_list.html'

class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'MyCourses/mailing_detail.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'MyCourses/mailing_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'MyCourses/mailing_form.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'MyCourses/mailing_confirm_delete.html'
    success_url = '/mailings/'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)
