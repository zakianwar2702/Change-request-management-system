import json
import csv

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


def get_ticket_report_data():
    total = SupportTicket.objects.count()
    summary = {
        'open': SupportTicket.objects.filter(status='OPEN').count(),
        'in_progress': SupportTicket.objects.filter(status='IN_PROGRESS').count(),
        'resolved': SupportTicket.objects.filter(status='RESOLVED').count(),
        'closed': SupportTicket.objects.filter(status='CLOSED').count(),
        'total': total,
    }
    by_status_qs = SupportTicket.objects.values('status').annotate(count=Count('id')).order_by('status')
    by_priority_qs = SupportTicket.objects.values('priority').annotate(count=Count('id')).order_by('priority')
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

    return {
        'summary': summary,
        'total': total,
        'by_status': by_status,
        'by_priority': by_priority,
        'recent_week': recent_week,
        'monthly': monthly,
    }


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
    report_data = get_ticket_report_data()
    created = request.GET.get('created') == '1'

    context = {
        'summary': report_data['summary'],
        'tickets': tickets,
        'created': created,
    }
    return render(request, 'support/dashboard.html', context)


def create_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('support_dashboard')}?created=1")
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
    report_data = get_ticket_report_data()
    recent_tickets = [serialize_ticket(ticket) for ticket in SupportTicket.objects.order_by('-created_at')[:6]]
    return JsonResponse({'summary': report_data['summary'], 'recent_tickets': recent_tickets})


@require_http_methods(['GET'])
def api_dashboard_statistics(request):
    report_data = get_ticket_report_data()
    return JsonResponse({
        'total': report_data['total'],
        'by_status': report_data['by_status'],
        'by_priority': report_data['by_priority'],
        'recent_week': report_data['recent_week'],
        'monthly': report_data['monthly'],
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
    report_data = get_ticket_report_data()

    context = {
        'total': report_data['total'],
        'by_status': report_data['by_status'],
        'by_priority': report_data['by_priority'],
        'recent_week': report_data['recent_week'],
        'monthly': report_data['monthly'],
    }
    return render(request, 'support/statistics.html', context)


def report_csv(request):
    report_data = get_ticket_report_data()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="support_tickets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Support Ticket Report'])
    writer.writerow([])
    writer.writerow(['Summary'])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Total Tickets', report_data['total']])
    writer.writerow(['Open', report_data['summary']['open']])
    writer.writerow(['In Progress', report_data['summary']['in_progress']])
    writer.writerow(['Resolved', report_data['summary']['resolved']])
    writer.writerow(['Closed', report_data['summary']['closed']])
    writer.writerow(['Recent (7d)', report_data['recent_week']])
    writer.writerow([])
    writer.writerow(['Status Breakdown'])
    writer.writerow(['Status', 'Count'])
    for status, count in report_data['by_status'].items():
        writer.writerow([status, count])
    writer.writerow([])
    writer.writerow(['Priority Breakdown'])
    writer.writerow(['Priority', 'Count'])
    for priority, count in report_data['by_priority'].items():
        writer.writerow([priority, count])
    writer.writerow([])
    writer.writerow(['Monthly Activity'])
    writer.writerow(['Month', 'Count'])
    for row in report_data['monthly']:
        writer.writerow([row['month'], row['count']])
    writer.writerow([])
    writer.writerow(['Ticket Details'])
    writer.writerow(['ID', 'Title', 'Requester', 'Status', 'Priority', 'Created At', 'Updated At'])

    for t in SupportTicket.objects.order_by('-created_at'):
        writer.writerow([t.id, t.title, t.requester, t.status, t.priority, t.created_at.isoformat(), t.updated_at.isoformat()])

    return response
