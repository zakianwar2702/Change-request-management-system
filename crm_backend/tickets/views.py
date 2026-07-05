from approvals.models import Approval
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ChangeRequest, DeveloperAssignment
from .serializers import (
    ChangeRequestSerializer,
    DeveloperAssignmentSerializer,
)

from django.contrib.auth.models import User


# ----------------------------
# Create Ticket API
# ----------------------------
@api_view(['POST'])
def create_ticket(request):

    serializer = ChangeRequestSerializer(data=request.data)

    if serializer.is_valid():
        ticket = serializer.save()

        Approval.objects.create(
            ticket=ticket,
            level=1
        )

        Approval.objects.create(
            ticket=ticket,
            level=2
        )

        return Response(
            {
                "message": "Ticket Created Successfully",
                "data": serializer.data
            },
            status=201
        )

    return Response(
        {
            "errors": serializer.errors
        },
        status=400
    )
# ----------------------------
# View All Tickets API
# ----------------------------
@api_view(['GET'])
def view_tickets(request):

    tickets = ChangeRequest.objects.all().order_by('-created_at')

    serializer = ChangeRequestSerializer(
        tickets,
        many=True
    )

    return Response(serializer.data)
# ----------------------------
# View All Tickets API
# ----------------------------
# ----------------------------
# Get Developers API
# ----------------------------
@api_view(['GET'])
def developers(request):

    users = User.objects.all()

    data = []

    for user in users:

        data.append({
            "id": user.id,
            "username": user.username
        })


    return Response(data)


# ----------------------------
# Update Ticket API
# ----------------------------
@api_view(['PUT'])
def update_ticket(request, ticket_id):

    try:
        ticket = ChangeRequest.objects.get(id=ticket_id)

    except ChangeRequest.DoesNotExist:
        return Response({
            "error": "Ticket Not Found"
        })

    serializer = ChangeRequestSerializer(
        ticket,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# ----------------------------
# Dashboard Summary API
# ----------------------------
@api_view(['GET'])
def summary(request):

    total = ChangeRequest.objects.count()
    open_count = ChangeRequest.objects.filter(status="Open").count()
    in_progress = ChangeRequest.objects.filter(status="In Progress").count()
    closed = ChangeRequest.objects.filter(status="Closed").count()

    recent = ChangeRequest.objects.order_by("-created_at")[:5]

    recent_data = []

    for ticket in recent:
        recent_data.append({
            "id": ticket.ticket_number,
            "title": ticket.project_name,
            "status": ticket.status,
            "requester": ticket.employee_name,
        })

    return Response({
        "summary": {
            "total": total,
            "open": open_count,
            "in_progress": in_progress,
            "resolved": 0,
            "closed": closed
        },
        "recent_tickets": recent_data
    })


# ----------------------------
# Assign Developer API
# ----------------------------
@api_view(['POST'])
def assign_developer(request):

    try:
        ticket = ChangeRequest.objects.get(
            id=request.data.get("change_request")
        )

        developer = User.objects.get(
            id=request.data.get("developer")
        )

    except (ChangeRequest.DoesNotExist, User.DoesNotExist):
        return Response({
            "error": "Invalid Ticket or Developer"
        }, status=404)


    assignment, created = DeveloperAssignment.objects.update_or_create(
        change_request=ticket,
        defaults={
            "developer": developer,
            "status": "Assigned"
        }
    )


    serializer = DeveloperAssignmentSerializer(assignment)

    return Response(serializer.data)


# ----------------------------
# Update Status API
# ----------------------------
@api_view(['PUT'])
def update_status(request, assignment_id):

    try:
        assignment = DeveloperAssignment.objects.get(
            id=assignment_id
        )

    except DeveloperAssignment.DoesNotExist:
        return Response({
            "error": "Assignment Not Found"
        }, status=404)


    assignment.status = request.data.get(
        "status",
        assignment.status
    )

    assignment.save()

    serializer = DeveloperAssignmentSerializer(assignment)

    return Response(serializer.data)


# ----------------------------
# Developer Dashboard API
# ----------------------------
@api_view(['GET'])
def developer_dashboard(request, developer_id):

    assignments = DeveloperAssignment.objects.filter(
        developer_id=developer_id
    )

    serializer = DeveloperAssignmentSerializer(
        assignments,
        many=True
    )

    return Response(serializer.data)