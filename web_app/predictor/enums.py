from django.db.models import TextChoices


class Gender(TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'