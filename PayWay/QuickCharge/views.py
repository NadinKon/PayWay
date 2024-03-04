from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Order, Item
import stripe
from django.conf import settings

# Установка ключа API Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    context = {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'item_detail.html', context)


def create_payment_intent_for_order(request, id):
    order = get_object_or_404(Order, pk=id)

    # Используем метод total_cost модели Order для расчета итоговой суммы
    total = order.total_cost()

    # Валюта заказа (принимаем, что все товары в заказе имеют одинаковую валюту)
    currency = order.items.first().currency

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Преобразуем в наименьшие денежные единицы
            currency=currency,
            metadata={'order_id': order.id}
        )
        return JsonResponse({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
