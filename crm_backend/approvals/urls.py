from django.urls import path
from . import views

urlpatterns = [
    path("level1/", views.level1, name="level1"),
    path("level2/", views.level2, name="level2"),
    path("approve/<int:approval_id>/", views.approve, name="approve"),
    path("history/<int:ticket_id>/", views.history, name="history"),
]