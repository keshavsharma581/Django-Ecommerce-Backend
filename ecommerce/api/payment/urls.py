from django.urls import path, include
from . import views


urlpatterns = [
    path('get_token/<str:id>/<str:token>', views.generate_token, name='payment.generate_token'),
    path('process_payment/<str:id>/<str:token>', views.process_payment, name='payment.process_payment'),
]