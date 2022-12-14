# Generated by Django 4.1.4 on 2022-12-13 11:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('measurement_unit', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='positions')),
                ('price', models.PositiveSmallIntegerField()),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('text', models.TextField()),
                ('category', models.ManyToManyField(related_name='positions', to='api.category')),
                ('ingredients', models.ManyToManyField(related_name='positions', to='api.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientsInPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_position', to='api.ingredient')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_position', to='api.position')),
            ],
        ),
    ]
