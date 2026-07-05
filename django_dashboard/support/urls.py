from django.urls import path
from .views import (
    support_dashboard, create_ticket, statistics, report_csv,
    api_dashboard_summary, api_dashboard_statistics,
    api_ticket_list, api_ticket_detail,
)

urlpatterns = [
    path('support_dashboard/', support_dashboard, name='support_dashboard'),
    path('create/', create_ticket, name='create_ticket'),
    path('stats/', statistics, name='statistics'),
    path('report/csv/', report_csv, name='report_csv'),
    path('api/summary/', api_dashboard_summary, name='api_dashboard_summary'),
    path('api/statistics/', api_dashboard_statistics, name='api_dashboard_statistics'),
    path('api/tickets/', api_ticket_list, name='api_ticket_list'),
    path('api/tickets/<int:ticket_id>/', api_ticket_detail, name='api_ticket_detail'),
]
