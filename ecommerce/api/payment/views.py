from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree


# Create your views here.

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='qxg7qdpvzpmvjjp5',
    public_key='wz89p9yjwnqthw2z',
    private_key='70e45f93271bc974f99796488805c21f'
  )
)


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
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid Session, Please Login Again.'})

    client_token = gateway.client_token.generate({
        "customer_id": id
    })

    return JsonResponse({'clientToken': client_token, 'success': True})


@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid Session, Please Login Again.'})

    nonce_from_the_client = request.POST['paymentMethodNonce']
    amount_from_the_client = request.POST['amount']

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({
            'success': result.is_success,
            'transaction': {
                'id': result.transaction.id,
                'amount': result.transaction.amount
            }
        })
    else:
        return JsonResponse({'success': False, 'error': True, 'message': 'Error in processing Payment'})
