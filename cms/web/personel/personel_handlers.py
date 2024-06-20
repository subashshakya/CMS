from ..models import Personel
from django.http import JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ..utils.util import *
from django.db.models import Q
import json

PERSONEL_REQUIRED_FIELDS = ["title", "first_name", "last_name", "phone_number", "email"]


def create_personel(request):
    try:
        personel = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse(
            {"success": False, "message": "Invalid JSON format. Could not parse JSON."},
            status=400,
        )
    request_fields = personel.keys()
    missing_fields = find_missing_fields(PERSONEL_REQUIRED_FIELDS, request_fields)
    if missing_fields:
        return JsonResponse(
            {"success": False, "message": "Missing required fields"}, status=400
        )
    new_personel = Personel(
        title=personel.title,
        first_name=personel.first_name,
        middle_name=personel.middle_name,
        last_name=personel.last_name,
        email=personel.email,
        available_time=personel.available_time,
        phone_number=personel.phone_number,
        specialization_desc=personel.specialization_desc,
    )
    try:
        new_personel.save()
        return JsonResponse(
            {"success": True, "message": "Successfully created personel"}, status=201
        )
    except ValidationError as e:
        return JsonResponse({"success": False, "message": e}, status=400)
    except Exception:
        return JsonResponse(
            {"success": False, "message": "Internal server error"}, status=500
        )


def get_personel(request, id):
    try:
        personel_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Please send a valid id for personel"},
            status=400,
        )
    try:
        personel = Personel.objects.get(pk=personel_id)
        return JsonResponse({"success": True, "data": personel}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Could not find requested personel"},
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": "Internal server error."}, status=500
        )


def update_personel(request, id):
    try:
        personel_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Please send a valid id for personel"},
            status=400,
        )
    try:
        personel_to_update = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Invalid JSON format."}, status=400
        )
    try:
        personel = Personel.objects.get(pk=id)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Could not find requested personel"},
            status=404,
        )
    updated_personel = update_fields(personel, personel_to_update)
    try:
        update_personel.save()
        return JsonResponse(
            {
                "success": True,
                "message": "Successfully updated personel " + personel_id,
                "data": updated_personel,
            },
            status=201,
        )
    except ValidationError:
        return JsonResponse(
            {"success": False, "message": "Could not validate the values for personel"},
            status=400,
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": e}, status=500)


def delete_personel(request, id):
    try:
        personel_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Please send a valid id for personel"},
            status=400,
        )
    try:
        Personel.objects.delete(pk=personel_id)
        return JsonResponse(
            {"success": True, "message": "Successfully deleted personel."}, status=200
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Could not find requested personel"},
            status=404,
        )
    except Exception:
        return JsonResponse(
            {"success": False, "message": "Internal server error."}, status=500
        )
