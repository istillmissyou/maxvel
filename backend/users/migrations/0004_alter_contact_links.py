# Generated by Django 4.1.4 on 2022-12-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_link_contact_contact_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='links',
            field=models.ManyToManyField(related_name='contact', to='users.link'),
        ),
    ]