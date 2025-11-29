from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User


# Create your models here.
class Document(models.Model): # Документ
    series = models.IntegerField() # Серия
    number = models.IntegerField() # Номер
    date_of_issue = models.DateField() # Дата выдачи
    issued_by = models.CharField(max_length=200) # Кем выдан

class Category(models.Model): # Категория
    name = models.CharField(max_length=50) # Название
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена
    description = models.TextField() # Описание

class Item(models.Model): # Предмет
    name = models.CharField(max_length=50) # Название

class Service(models.Model): # Услуга
    name = models.CharField(max_length=50) # Название
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена
    description = models.TextField() # Описание
    available_to_guest = models.BooleanField(default=False)

class Guest(models.Model): # Гость
    name = models.CharField(max_length=200) # ФИО
    phone_number = models.CharField(max_length=16) # Номер телефона в формате +7(777)777-77-77
    date_of_birth = models.DateField() # Дата рождения
    document = models.ForeignKey(Document, on_delete=CASCADE, related_name="guest", null=True, blank=True) # Документ (может быть пустой)
    discount = models.IntegerField() # Скидка в процентах
    user_profile = models.ForeignKey(User, on_delete=CASCADE, related_name="guest_info", null=True, blank=True)

class Room(models.Model): # Номер
    floor = models.IntegerField() # Этаж
    room_count = models.IntegerField() # Количество комнат
    berths_count = models.IntegerField() # Количество спальных мест
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="rooms") # Категория

class Equipment(models.Model): # Оснащение
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="equipment") # Категория
    item = models.ForeignKey(Item, on_delete=CASCADE, related_name="equipment") # Предмет

    # Объявление о том, что связка категории и предмета уникальна
    # Но в базе данных все равно сгенерируется отдельное поле первичного ключа
    class Meta:
        unique_together = (('category', 'item'),)

class Reservation(models.Model): # Бронирование
    client = models.ForeignKey(Guest, on_delete=CASCADE, related_name="reservations") # Клиент
    room = models.ForeignKey(Room, on_delete=CASCADE, related_name="reservations") # Номер
    move_in_date = models.DateField() # Дата заезда
    move_out_date = models.DateField() # Дата выезда
    price = models.DecimalField(max_digits=10, decimal_places=2) # Стоимость
    paid = models.BooleanField(default=False) # Факт оплаты

class ProvisionOfService(models.Model): # Оказание услуги
    reservation = models.ForeignKey(Reservation, on_delete=CASCADE, related_name="provisions") # Бронирование
    service = models.ForeignKey(Service, on_delete=CASCADE, related_name="provisions") # Услуга
    count = models.IntegerField() # Количество
    date_of_provision = models.DateField() # Дата оказания