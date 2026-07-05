from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Approval
from .serializers import ApprovalSerializer

from tickets.models import ChangeRequest



# ----------------------------
# Level 1 Pending Approvals
# ----------------------------
@api_view(["GET"])
def level1(request):

    approvals = Approval.objects.filter(
        level=1,
        status="Pending"
    )

    serializer = ApprovalSerializer(
        approvals,
        many=True
    )

    return Response(serializer.data)




# ----------------------------
# Level 2 Pending Approvals
# ----------------------------
@api_view(["GET"])
def level2(request):

    approvals = Approval.objects.filter(
        level=2,
        status="Pending"
    )

    serializer = ApprovalSerializer(
        approvals,
        many=True
    )

    return Response(serializer.data)





# ----------------------------
# Approve / Reject
# ----------------------------
@api_view(["PUT"])
def approve(request, approval_id):

    try:

        approval = Approval.objects.get(
            id=approval_id
        )


    except Approval.DoesNotExist:

        return Response(
            {
                "error":"Approval not found"
            },
            status=404
        )



    new_status = request.data.get(
        "status"
    )


    if new_status not in [
        "Approved",
        "Rejected"
    ]:

        return Response(
            {
                "error":"Invalid status"
            },
            status=400
        )



    approval.status = new_status

    approval.remarks = request.data.get(
        "remarks",
        ""
    )

    approval.save()



    ticket = approval.ticket





    # LEVEL 1 APPROVED
    # Make sure Level 2 exists
    if (
        approval.level == 1
        and new_status == "Approved"
    ):


        level2_exists = Approval.objects.filter(

            ticket=ticket,

            level=2

        ).exists()



        if not level2_exists:


            Approval.objects.create(

                ticket=ticket,

                level=2,

                status="Pending"

            )







    # LEVEL 2 APPROVED
    # Send to developer stage

    if (

        approval.level == 2

        and new_status == "Approved"

    ):


        ticket.status = "In Progress"

        ticket.save()





    return Response({

        "message":"Approval updated",

        "ticket_status":ticket.status

    })







# ----------------------------
# History
# ----------------------------
@api_view(["GET"])
def history(request,ticket_id):

    approvals = Approval.objects.filter(

        ticket_id=ticket_id

    )


    serializer = ApprovalSerializer(

        approvals,

        many=True

    )


    return Response(serializer.data)