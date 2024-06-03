from django.urls import path
from .views import HomeView, MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = 'MyCourses'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_confirm_delete'),
]