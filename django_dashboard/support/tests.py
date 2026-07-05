from django.test import TestCase
from django.urls import reverse

from .models import SupportTicket


class SupportReportingTests(TestCase):
    def setUp(self):
        SupportTicket.objects.create(title='Login issue', requester='Asha', status='OPEN', priority='High')
        SupportTicket.objects.create(title='Billing issue', requester='Ravi', status='RESOLVED', priority='Medium')

    def test_dashboard_includes_statistics_and_report_links(self):
        response = self.client.get(reverse('support_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Statistics')
        self.assertContains(response, 'Download CSV')

    def test_report_csv_contains_summary_and_ticket_rows(self):
        response = self.client.get(reverse('report_csv'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Summary', content)
        self.assertIn('Total Tickets', content)
        self.assertIn('Open', content)
        self.assertIn('Resolved', content)
        self.assertIn('Login issue', content)

    def test_create_ticket_page_includes_project_field(self):
        response = self.client.get(reverse('create_ticket'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('project', response.context['form'].fields)
