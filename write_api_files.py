from pathlib import Path

views_path = Path('django_dashboard/support/views.py')
urls_path = Path('django_dashboard/support/urls.py')

views_content = '''import json

from datetime import timedelta

from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import SupportTicket
from .forms import SupportTicketForm


def support_dashboard(request):
    if SupportTicket.objects.count() == 0:
        sample_tickets = [
            {
                'title': 'Cannot access account',
                'requester': 'Priya Patel',
                'status': 'OPEN',
                'priority': 'High',
            },
            {
                'title': 'Billing discrepancy on invoice',
                'requester': 'Rahul Singh',
                'status': 'IN_PROGRESS',
                'priority': 'Medium',
            },
            {
                'title': 'New user onboarding request',
                'requester': 'Sneha Sharma',
                'status': 'RESOLVED',
                'priority': 'Low',
            },
        ]
        for ticket_data in sample_tickets:
            SupportTicket.objects.create(**ticket_data)

    tickets = SupportTicket.objects.order_by('-created_at')[:6]
    summary = {
        'open': SupportTicket.objects.filter(status='OPEN').count(),
        'in_progress': SupportTicket.objects.filter(status='IN_PROGRESS').count(),
        'resolved': SupportTicket.objects.filter(status='RESOLVED').count(),
        'closed': SupportTicket.objects.filter(status='CLOSED').count(),
        'total': SupportTicket.objects.count(),
    }

    context = {
        'summary': summary,
        'tickets': tickets,
    }
    return render(request, 'support/dashboard.html', context)


def create_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('support_dashboard'))
    else:
        form = SupportTicketForm()

    return render(request, 'support/create_ticket.html', {'form': form})


def serialize_ticket(ticket):
    return {
        'id': ticket.id,
        'title': ticket.title,
        'requester': ticket.requester,
        'status': ticket.status,
        'priority': ticket.priority,
        'created_at': ticket.created_at.isoformat(),
        'updated_at': ticket.updated_at.isoformat(),
    }


@require_http_methods(['GET'])
def api_dashboard_summary(request):
    summary = {
        'open': SupportTicket.objects.filter(status='OPEN').count(),
        'in_progress': SupportTicket.objects.filter(status='IN_PROGRESS').count(),
        'resolved': SupportTicket.objects.filter(status='RESOLVED').count(),
        'closed': SupportTicket.objects.filter(status='CLOSED').count(),
        'total': SupportTicket.objects.count(),
    }
    recent_tickets = [serialize_ticket(ticket) for ticket in SupportTicket.objects.order_by('-created_at')[:6]]
    return JsonResponse({'summary': summary, 'recent_tickets': recent_tickets})


@require_http_methods(['GET'])
def api_dashboard_statistics(request):
    total = SupportTicket.objects.count()
    by_status_qs = SupportTicket.objects.values('status').annotate(count=Count('id'))
    by_priority_qs = SupportTicket.objects.values('priority').annotate(count=Count('id'))
    recent_week = SupportTicket.objects.filter(created_at__gte=now() - timedelta(days=7)).count()
    monthly_qs = (
        SupportTicket.objects
        .extra({'month': "strftime('%Y-%m', created_at)"})
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    by_status = {item['status']: item['count'] for item in by_status_qs}
    by_priority = {item['priority']: item['count'] for item in by_priority_qs}
    monthly = list(monthly_qs)
    return JsonResponse({
        'total': total,
        'by_status': by_status,
        'by_priority': by_priority,
        'recent_week': recent_week,
        'monthly': monthly,
    })


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api_ticket_list(request):
    if request.method == 'GET':
        tickets = SupportTicket.objects.order_by('-created_at')
        return JsonResponse({'tickets': [serialize_ticket(ticket) for ticket in tickets]})

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON payload')

    form = SupportTicketForm(payload)
    if form.is_valid():
        ticket = form.save()
        return JsonResponse(serialize_ticket(ticket), status=201)

    return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_ticket_detail(request, ticket_id):
    try:
        ticket = SupportTicket.objects.get(pk=ticket_id)
    except SupportTicket.DoesNotExist:
        return JsonResponse({'error': 'SupportTicket not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(serialize_ticket(ticket))

    if request.method == 'DELETE':
        ticket.delete()
        return HttpResponse(status=204)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON payload')

    form = SupportTicketForm(payload, instance=ticket)
    if form.is_valid():
        ticket = form.save()
        return JsonResponse(serialize_ticket(ticket))

    return JsonResponse({'errors': form.errors}, status=400)


def statistics(request):
    total = SupportTicket.objects.count()
    by_status_qs = SupportTicket.objects.values('status').annotate(count=Count('id'))
    by_priority_qs = SupportTicket.objects.values('priority').annotate(count=Count('id'))

    # Recent activity
    recent_week = SupportTicket.objects.filter(created_at__gte=now()-timedelta(days=7)).count()

    # Monthly counts (SQLite strftime)
    monthly_qs = (SupportTicket.objects
                  .extra({
                      'month': "strftime('%Y-%m', created_at)"
                  })
                  .values('month')
                  .annotate(count=Count('id'))
                  .order_by('month'))

    by_status = {item['status']: item['count'] for item in by_status_qs}
    by_priority = {item['priority']: item['count'] for item in by_priority_qs}
    monthly = list(monthly_qs)

    context = {
        'total': total,
        'by_status': by_status,
        'by_priority': by_priority,
        'recent_week': recent_week,
        'monthly': monthly,
    }
    return render(request, 'support/statistics.html', context)


def report_csv(request):
    # Return a CSV export of all support tickets
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="support_tickets.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Requester', 'Status', 'Priority', 'Created At', 'Updated At'])

    for t in SupportTicket.objects.order_by('-created_at'):
        writer.writerow([t.id, t.title, t.requester, t.status, t.priority, t.created_at.isoformat(), t.updated_at.isoformat()])

    return response
'''

urls_content = '''from django.urls import path
from .views import (
    support_dashboard, create_ticket, statistics, report_csv,
    api_dashboard_summary, api_dashboard_statistics,
    api_ticket_list, api_ticket_detail,
)

urlpatterns = [
    path('', support_dashboard, name='support_dashboard'),
    path('create/', create_ticket, name='create_ticket'),
    path('stats/', statistics, name='statistics'),
    path('report/csv/', report_csv, name='report_csv'),
    path('api/summary/', api_dashboard_summary, name='api_dashboard_summary'),
    path('api/statistics/', api_dashboard_statistics, name='api_dashboard_statistics'),
    path('api/tickets/', api_ticket_list, name='api_ticket_list'),
    path('api/tickets/<int:ticket_id>/', api_ticket_detail, name='api_ticket_detail'),
]
'''

views_path.write_text(views_content, encoding='utf-8')
urls_path.write_text(urls_content, encoding='utf-8')
print('Wrote views.py and urls.py')
