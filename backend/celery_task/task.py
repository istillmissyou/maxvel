from api.models import ShoppingCart
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from maxvel.celery import app


@app.task
def send_email_with_shopping_card(pk):
    """Отправка на почту"""
    shopping_card = ShoppingCart.objects.get(id=pk)
    topic = "Новый заказ"
    email_from = settings.EMAIL_HOST_USER
    email = [settings.EMAIL_USER]
    message = ''
    for position in shopping_card.positions_in_cart.all():
        message += position.position.name
    message += str(shopping_card.all_amount)
    message += shopping_card.name_user
    message += shopping_card.phone
    message += shopping_card.email
    message += shopping_card.address
    message += str(shopping_card.date_start)
    message += shopping_card.comment
    send_mail(
        topic,
        message,
        email_from,
        email
    )
