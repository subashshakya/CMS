from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, blank=False)
    password = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Phone number must be exactly 10 digits",
                code="invalid_phone_number",
            )
        ],
        blank=False,
    )
    country_code = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex=r"^\+\d{3}$", message="Invalid Country Code")],
    )
    first_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)


class Service(models.Model):
    name = models.CharField(max_length=30, blank=False)
    review = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=False)
    price = models.FloatField(blank=False)
    benefits = models.CharField()
    number_of_appointments = models.IntegerField()


class Personel(models.Model):
    title = models.CharField(max_length=20, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField()
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField()
    available_time = models.DurationField()
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Phone number must be exactly 10 digits",
                code="invalid_phone_number",
            )
        ],
        blank=False,
    )
    specialization_desc = models.TextField()


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    date_time = models.DateTimeField(blank=False)
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=30, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    parent_category = models.CharField()
    image = models.ImageField()
    reviews_count = models.IntegerField()
    description = models.TextField()
    sku = models.CharField(max_length=15)
    avg_rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DateTimeField()
    message = models.TextField()

    class Meta:
        abstract = True


class ServiceBooking(Booking):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    needs = models.TextField()


class ProductBooking(Booking):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    needs = models.TextField()
