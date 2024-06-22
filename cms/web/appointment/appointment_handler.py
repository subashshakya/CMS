from ..models import Appointment, Service, User, Personel
from django.http import JsonResponse
from django.core.exceptions import ValueError, ObjectDoesNotExist, ValidationError
from ..utils.util import *
import json


APPOINTMENT_REQUIRED_FIELD = ["service", "user", "date_time", "personel"]


def create_appointment(request):
    try:
        appointment_request = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Invalid JSON format."}, status=400
        )
    missing_fields = find_missing_fields(
        APPOINTMENT_REQUIRED_FIELD, appointment_request.keys()
    )
    if missing_fields:
        return JsonResponse(
            {"success": False, "message": "Missing fields for creating an appointment"},
            status=400,
        )
    try:
        service_check = Service.objects.get(pk=appointment_request.service)
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Could not find requested service. Id invalid.",
            },
            status=404,
        )
    try:
        user_check = User.objects.get(pk=appointment_request.user)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Could not find requested user. Id invalid."},
            status=404,
        )
    try:
        personel_check = Personel.objects.get(pk=appointment_request.personel)
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Could not find requested Personel. Id invalid.",
            },
            status=404,
        )
    if service_check and user_check and personel_check:
        new_appointment = Appointment(
            service=appointment_request.service,
            user=appointment_request.user,
            date_time=appointment_request.date_time,
            personel=appointment_request.personel,
        )
        try:
            new_appointment.save()
            return JsonResponse(
                {"success": True, "message": "Successfully created appointment."},
                status=201,
            )
        except ValidationError:
            return JsonResponse(
                {"success": False, "message": "Could not validate request fields"},
                status=400,
            )
        except Exception:
            return JsonResponse(
                {"success": False, "message": "Internal server error."}, status=500
            )


def get_appointment(request, id):
    if not id:
        try:
            appointments = Appointment.objects.all()
            return JsonResponse({"success": False, "data": [appointments]}, status=200)
        except Exception:
            return JsonResponse(
                {"success": False, "message": "Internal server error"}, status=500
            )
    else:
        try:
            appointment_id = int(id)
        except ValueError:
            return JsonResponse(
                {"success": False, "message": "Unprocessable entity. Invalid id"},
                status=422,
            )
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            return JsonResponse({"success": True, "data": appointment}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Could not find the requested appointment",
                },
                status=404,
            )
        except Exception:
            return JsonResponse(
                {"success": False, "message": "Internal server error"}, status=500
            )


def update_appointment(request, id):
    try:
        appointment_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Unprocessable entity. Invalid id format."},
            status=422,
        )
    try:
        appointment = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Invalid JSON format."}, status=400
        )
    missing_fields = find_missing_fields(APPOINTMENT_REQUIRED_FIELD, appointment.keys())
    if missing_fields:
        return JsonResponse(
            {
                "success": False,
                "message": "Missing fields in request for updating appointment.",
            },
            status=400,
        )
    try:
        appointment_from_db = Appointment.objects.get(pk=appointment_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Not able to find appointment from the ID."},
            status=404,
        )
    updated_appointment = update_fields(appointment_from_db, appointment)
    try:
        update_appointment.save()
        return JsonResponse(
            {
                "success": False,
                "message": "Successfully updated appointment.",
                "data": update_appointment,
            },
            status=200,
        )
    except ValidationError:
        return JsonResponse(
            {"success": False, "message": "Could not validate field values."},
            status=400,
        )
    except Exception:
        return JsonResponse(
            {"success": False, "message": "Internal server error"}, status=500
        )


def delete_appointment(request, id):
    try:
        appointment_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Unprocessable entity. Invalid id format."},
            status=422,
        )
    try:
        appointment_from_db = Appointment.objects.delete(pk=appointment_id)
        return JsonResponse(
            {"success": True, "message": "Successfully deleted appointment."},
            status=200,
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Not able to find appointment from the ID."},
            status=404,
        )
    except Exception:
        return JsonResponse(
            {"success": False, "message": "Internal server error"}, status=500
        )
