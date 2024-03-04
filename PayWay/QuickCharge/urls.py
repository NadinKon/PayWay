from django.urls import path
from .views import item_detail, create_payment_intent_for_order

urlpatterns = [
    path('item/<int:id>/', item_detail, name='item_detail'),
    path('buy/<int:id>/', create_payment_intent_for_order, name='create_payment_intent_for_order'),
]
