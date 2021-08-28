from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .serializers import OrderSerializer
from .models import Order


def validate_user_session(id, token):
    user_model = get_user_model()

    try:
        user = user_model.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except user_model.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Please re-login'})

    if request.method == 'POST':
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']
        total_products = len(products.split(',')[:-1])

        user_model = get_user_model()

        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return JsonResponse({'error':'User Does not exist'})

        order = Order(user=user, product_names=products, total_products=total_products,
                      transaction_id=transaction_id, total_amount=amount)

        order.save()
        return JsonResponse({'success': True, 'error': False, 'message': 'Order Placed Successfully'})

    return JsonResponse({'error': 'Send a POST request with valid parameters.'})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

