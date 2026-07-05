from rest_framework import serializers
from .models import ChangeRequest, DeveloperAssignment


class ChangeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangeRequest
        fields = "__all__"


class DeveloperAssignmentSerializer(serializers.ModelSerializer):

    developer_name = serializers.CharField(
        source="developer.username",
        read_only=True
    )

    ticket_number = serializers.CharField(
        source="change_request.ticket_number",
        read_only=True
    )

    class Meta:
        model = DeveloperAssignment
        fields = [
            "id",
            "change_request",
            "ticket_number",
            "developer",
            "developer_name",
            "status",
            "assigned_at",
            "updated_at",
        ]