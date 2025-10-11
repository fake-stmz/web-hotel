from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Document(models.Model):
    series = models.IntegerField()
    number = models.IntegerField()
    date_of_issue = models.DateField()
    issued_by = models.CharField(max_length=200)

class Category(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Item(models.Model):
    name = models.CharField(max_length=50)

class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Guest(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=16)
    date_of_birth = models.DateField()
    document = models.ForeignKey(Document, on_delete=CASCADE, related_name="guest", null=True, blank=True)
    discount = models.IntegerField()

class Room(models.Model):
    floor = models.IntegerField()
    room_count = models.IntegerField()
    berths_count = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="rooms")

class Equipment(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="equipment")
    item = models.ForeignKey(Item, on_delete=CASCADE, related_name="equipment")

    class Meta:
        unique_together = (('category_id', 'item_id'),)

class Reservation(models.Model):
    client = models.ForeignKey(Guest, on_delete=CASCADE, related_name="reservations")
    room = models.ForeignKey(Room, on_delete=CASCADE, related_name="reservations")
    move_in_date = models.DateField()
    move_out_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

class ProvisionOfService(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=CASCADE, related_name="provisions")
    service = models.ForeignKey(Service, on_delete=CASCADE, related_name="provisions")
    count = models.IntegerField()
    date_of_provision = models.DateField()