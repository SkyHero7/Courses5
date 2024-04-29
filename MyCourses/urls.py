from django.urls import path
from .views import home, mailing_list, mailing_create, mailing_update, mailing_delete

app_name = 'MyCourses'

urlpatterns = [
    path('', home, name='index'),
    path('', mailing_list, name='mailing_list'),
    path('create/', mailing_create, name='mailing_form'),
    path('edit/<int:mailing_id>/', mailing_update, name='mailing_edit'),
    path('delete/<int:mailing_id>/', mailing_delete, name='mailing_confirm_delete'),

]
