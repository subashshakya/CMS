import json
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from ..models import Service
from utils.util import *
from django.core import serializers
from django.db.models import Q

SERVICE_REQUIRED_FIELDS = ["name", "description", "price"]


def add_service(request):
    try:
        service_data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"success": False, "message": e}, status=400)

    request_keys = service_data.keys()
    missing_fields = find_missing_fields(SERVICE_REQUIRED_FIELDS, request_keys)
    if missing_fields:
        return JsonResponse(
            {"success": False, "message": "Missing required fields"}, status=400
        )
    new_service = Service(
        name=service_data.name,
        review=service_data.review,
        description=service_data.description,
        price=service_data.price,
        benefits=service_data.benefits,
        number_of_appointments=service_data.number_of_appointments,
    )
    try:
        new_service.save()
        return JsonResponse(
            {"success": True, "message": "Successfully added service"}, status=201
        )
    except ValidationError as e:
        return JsonResponse({"success": False, "message": e}, status=400)


def get_service(request, id):
    try:
        int_id = int(id)
        service = Service.objects.get(pk=int_id)
    except ObjectDoesNotExist as e:
        return JsonResponse(
            {"success": False, "message": "Requested service does not exist"},
            status=404,
        )

    except ValueError as e:
        return JsonResponse({"success": False, "message": e}, status=400)

    except Exception as e:
        return JsonResponse({"success": False, "message": e}, status=500)

    contains_query_params = (
        request.GET.get("name_cont")
        and request.GET.get("price_gt")
        and request.GET.get("price_lt")
    )

    if not contains_query_params:
        try:
            service_json = serializers.serialize("json", [service])
            return JsonResponse(
                {
                    "success": True,
                    "message": "Request successful",
                    "data": service_json,
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": e}, status=500)
    else:
        name_cont = request.GET.get("name_cont")
        price_gt = float(request.GET.get("price_gt"))
        price_lt = float(request.GET.get("price_lt"))
        try:
            services = Service.objects.filter(
                Q(name__icontains=name_cont)
                & Q(price__lt=price_lt)
                & Q(price__gt=price_gt)
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Request successful",
                    "data": list(services),
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": e}, status=500)


def update_service(request, id):
    try:
        service_to_update = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse(
            {"success": False, "message": "Invalid json format"}, status=400
        )
    try:
        service_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Unprocessable entity"}, status=422
        )
    request_keys = service_to_update.keys()
    missing_fields = find_missing_fields(SERVICE_REQUIRED_FIELDS, request_keys)
    if missing_fields:
        return JsonResponse(
            {
                "success": False,
                "message": "Missing required fields to modify the current service",
            },
            status=400,
        )
    try:
        service = Service.objects.get(pk=id)
    except ObjectDoesNotExist as e:
        return JsonResponse(
            {
                "success": False,
                "message": "Could not find the requested service to update",
            },
            status=404,
        )
    service_update = {key: service_to_update[key] for key in service.keys()}
    try:
        service_update.save()
        return JsonResponse(
            {"success": True, "message": "Successfully updated service."}
        )
    except ValidationError as e:
        return JsonResponse(
            {"success": False, "message": "Could not validate the required data."},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": "Internal Server Error"}, status=500
        )


def delete_service(request, id):
    try:
        service_to_update = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse(
            {"success": False, "message": "Invalid json format"}, status=400
        )
    try:
        service_id = int(id)
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Unprocessable entity"}, status=422
        )
    request_keys = service_to_update.keys()
    missing_fields = find_missing_fields(SERVICE_REQUIRED_FIELDS, request_keys)
    if missing_fields:
        return JsonResponse(
            {
                "success": False,
                "message": "Missing required fields to modify the current service",
            },
            status=400,
        )
    try:
        service = Service.objects.delete(pk=id)
    except ObjectDoesNotExist as e:
        return JsonResponse(
            {
                "success": False,
                "message": "Could not find the requested service to update",
            },
            status=404,
        )
