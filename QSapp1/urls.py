from django.urls import path
from . import views

urlpatterns = [
    path('kiosk/', views.kiosk_view, name='kiosk'),
    path('kiosk/issue/<int:service_id>/', views.issue_ticket, name='issue_ticket'),
    path('', views.main_display, name='main_display'),
    path('staff/<int:counter_id>/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/call-next/<int:counter_id>/', views.call_next, name='call_next'),
    path('staff/skip/<int:ticket_id>/', views.skip_ticket, name='skip_ticket'),
    path('staff/recall/<int:ticket_id>/', views.recall_ticket, name='recall_ticket'),
    path('staff/start/<int:ticket_id>/', views.start_serving, name='start_serving'),
    path('staff/complete/<int:ticket_id>/', views.complete_ticket, name='complete_ticket'),
    path('staff/hold/<int:ticket_id>/', views.hold_ticket, name='hold_ticket'),
    path('staff/call-specific/<int:ticket_id>/', views.call_specific_ticket, name='call_specific'),
    path('staff/remove/<int:ticket_id>/', views.remove_ticket, name='remove_ticket'),
    path('staff/return-to-queue/<int:ticket_id>/', views.return_to_queue, name='return_to_queue'),
    path('issue/<int:service_id>/<int:counter_id>/', views.issue_ticket, name='issue_ticket'),
]