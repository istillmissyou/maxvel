from api.models import ShoppingCart
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from maxvel.celery import app
from users.models import CallMe


@app.task
def send_email_with_shopping_card(pk):
    """Отправка на почту"""
    shopping_card = ShoppingCart.objects.get(id=pk)
    topic = "Новый заказ"
    email_from = settings.EMAIL_HOST_USER
    email = [settings.EMAIL_USER]
    message = 'Пришел новый заказ'
    for position in shopping_card.positions_in_cart.all():
        message += position.position.name + '\n'
    message += str(shopping_card.all_amount) + '\n'
    message += shopping_card.name_user + '\n'
    message += shopping_card.phone + '\n'
    message += shopping_card.email + '\n'
    message += shopping_card.address + '\n'
    message += str(shopping_card.date_start) + '\n'
    message += shopping_card.comment + '\n'
    send_mail(
        topic,
        message,
        email_from,
        email
    )


@app.task
def send_email_with_call_me(pk):
    """Отправка на почту"""
    call_me = CallMe.objects.get(id=pk)
    topic = "Позвоните мне"
    email_from = settings.EMAIL_HOST_USER
    email = [settings.EMAIL_USER]
    message = 'Пришел новый заказ\n'
    message += 'телефон ' + call_me.phone + '\n'
    message += 'Коментарий ' + call_me.comment + '\n'
    send_mail(
        topic,
        message,
        email_from,
        email
    )
