from django.db import models
from django.contrib.auth.models import User

class ProfitableTransaction(models.Model):
    date = models.DateField(blank=False, verbose_name='Дата дохода')
    income_type = models.ManyToManyField('IncomeType', blank=True, verbose_name='Тип дохода')
    name = models.CharField(max_length=200, verbose_name='Наименование дохода')
    description = models.TextField(null=True, blank=True, verbose_name='Описание дохода')
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Сумма')

    def __str__(self):
        return self.name



class ExpenditureTransaction(models.Model):
    date = models.DateField(blank=False, verbose_name='Дата расхода')
    category = models.ManyToManyField('Category', blank=True, verbose_name='Категория расхода')
    name = models.CharField(max_length=200, verbose_name='Наименование расхода')
    description = models.TextField(null=True, blank=True, verbose_name='Описание расхода')
    meter = models.ManyToManyField('Meter', blank=True, verbose_name='Единица измерения товара/услуги')
    meter_quantity = models.DecimalField(null=True, max_digits=20, decimal_places=2, verbose_name='Количество измерителя')
    price_per_meter_unit = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена за единицу измерения')

    @property
    def total_cost(self):
        return round(self.meter_quantity * self.price_per_meter_unit, 2)

    def __str__(self):
        return self.name



class IncomeType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Meter(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


