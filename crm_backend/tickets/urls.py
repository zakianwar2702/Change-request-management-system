from django.urls import path
from . import views


urlpatterns = [

    # View all tickets
    path(
        '',
        views.view_tickets,
        name="view_tickets"
    ),


    # Create new request
    path(
        'create/',
        views.create_ticket,
        name="create_ticket"
    ),


    # Update ticket
    path(
        'update/<int:ticket_id>/',
        views.update_ticket,
        name="update_ticket"
    ),


    # Dashboard summary
    path(
        'summary/',
        views.summary,
        name="summary"
    ),


    # Assign developer
    path(
        'assign-developer/',
        views.assign_developer,
        name="assign_developer"
    ),


    # Get developers list
    path(
        'users/',
        views.developers,
        name="developers"
    ),


    # Update developer work status
    path(
        'status/<int:assignment_id>/',
        views.update_status,
        name="update_status"
    ),


    # Developer dashboard
    path(
        'developer/<int:developer_id>/',
        views.developer_dashboard,
        name="developer_dashboard"
    ),

]