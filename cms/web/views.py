from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import json
from .models import *
from .utils.util import *
from .service.service_handlers import *
from .personel.personel_handlers import *


@csrf_exempt
@require_http_methods(["POST"])
def user_signup(request):
    try:
        user_data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"success": False, "message": e}, status=400)
    required_fields = [
        "username",
        "password",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    ]
    request_fields = user_data.keys()

    missing_fields = [field for field in required_fields if field not in request_fields]
    if missing_fields:
        return JsonResponse(
            {"success": False, "message": "Missing fields in signup form"}, status=400
        )

    country_code = user_data.get("country_code")
    middle_name = user_data.get("middle_name")

    try:
        new_user = User(
            username=user_data.get("username"),
            password=user_data.get("password"),
            email=user_data.get("email"),
            phone_number=user_data.get("phone_number"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
        )
        if country_code:
            new_user.country_code = country_code
        if middle_name:
            new_user.middle_name = middle_name
        new_user.save()
        return JsonResponse(
            {"success": True, "message": "User signup successful"}, status=201
        )

    except ValidationError as e:
        return JsonResponse({"success": False, "message": e}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def user_sign_in(request):
    try:
        user_data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"success": False, "message": e}, status=400)

    required_fields = [
        "username",
        "password",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    ]
    request_fields = user_data.keys()
    missing_fields = [field for field in required_fields if field not in request_fields]
    if missing_fields:
        return JsonResponse(
            {"success": False, "message": "Missing required fields for sign-in"},
            status=400,
        )
    try:
        user = User.get(username=user_data.objects.get("username"))
    except ObjectDoesNotExist as e:
        return JsonResponse({"success": False, "message": e}, status=400)

    if (
        user.password == user_data.get("password")
        and user.email == user_data.get("email")
        and user.phone_number == user_data.get("phone_number")
        and user.first_name == user_data.get("first_name")
        and user.last_name == user_data.get("last_name")
    ):
        return JsonResponse(
            {"success": True, "message": "Sign-in successful"}, status=200
        )
    else:
        return JsonResponse(
            {"success": False, "message": "Could not match fields, please try again."},
            status=400,
        )


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def service(request, id):
    if id:
        if request.method == "GET":
            get_service(request, id)
        if request.method == "PUT":
            update_service(request, id)
        if request.method == "DELETE":
            delete_service(request, id)
    else:
        if request.method == "POST":
            add_service(request)


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def personel(request, id):
    if id:
        if request.method == "GET":
            get_personel(request, id)
        if request.method == "PUT":
            update_personel(request, id)
        if request.method == "DELETE":
            delete_personel(request, id)
    else:
        if request.method == "POST":
            create_personel(request)
