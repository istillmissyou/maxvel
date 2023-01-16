import phonenumbers
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Link(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=30,
        unique=True,
    )
    link = models.URLField(verbose_name='Ссылка', max_length=128)

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self):
        return self.link


class Contact(models.Model):
    links = models.ManyToManyField(
        Link,
        verbose_name='Ссылки',
        related_name='contact',
    )
    phone = models.CharField(verbose_name='Телефон', max_length=12)
    address = models.CharField(verbose_name='Адрес', max_length=1024)
    address_on_map = models.CharField(
        verbose_name='Адрес на карте',
        max_length=1024,
    )
    email = models.EmailField(verbose_name='Почта', max_length=255)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def validate_only_one_instance(self, obj):
        model = obj.__class__
        if (model.objects.count() > 0 and
                obj.id != model.objects.get().id):
            raise ValidationError("Можно создать только 1 контакт ")

    def clean(self):
        self.validate_only_one_instance(self)
        new_number = phonenumbers.parse(self.phone, "RU")
        print(new_number)
        if phonenumbers.is_valid_number(new_number) is False:
            raise ValidationError(_('Поле телефона не корректное'))
        # if len(self.phone) != 11:
        #     raise ValidationError(_('Поле телефона должно состоять из 11 цифр'))

    def __str__(self):
        return self.phone


class CallMe(models.Model):
    phone = models.CharField(verbose_name='Телефон', max_length=12)
    comment = models.CharField(verbose_name='Комментарий', max_length=1024)

    class Meta:
        verbose_name = 'Позвоните мне'
        verbose_name_plural = 'Позвоните мне'

    def clean(self):
        new_number = phonenumbers.parse(self.phone, "RU")
        print(new_number)
        if phonenumbers.is_valid_number(new_number) is False:
            raise ValidationError(_('Поле телефона не корректное'))
        # if len(self.phone) != 11:
        #     raise ValidationError(_('Поле телефона должно состоять из 11 цифр'))

    def __str__(self):
        return self.comment
