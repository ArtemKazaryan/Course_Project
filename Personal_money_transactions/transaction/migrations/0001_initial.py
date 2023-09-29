# Generated by Django 4.2.5 on 2023-09-28 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('meter_quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('price_per_meter_unit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('category', models.ManyToManyField(blank=True, to='transaction.category')),
                ('meter', models.ManyToManyField(blank=True, to='transaction.meter')),
                ('transaction_type', models.ManyToManyField(blank=True, to='transaction.transactiontype')),
            ],
        ),
    ]