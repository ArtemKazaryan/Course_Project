from django.db import models
from django.contrib.auth.models import User

class ProfitableTransaction(models.Model):
    date = models.DateField(blank=False)
    income_type = models.ManyToManyField('IncomeType', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name



class ExpenditureTransaction(models.Model):
    date = models.DateField(blank=False)
    category = models.ManyToManyField('Category', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    meter = models.ManyToManyField('Meter', blank=True)
    meter_quantity = models.DecimalField(null=True, max_digits=20, decimal_places=2)
    price_per_meter_unit = models.DecimalField(max_digits=20, decimal_places=2)

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


