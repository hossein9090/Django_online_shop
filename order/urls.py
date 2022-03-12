from django.urls import path

from order.views import add_user_order, user_open_order, remove_order_detail

urlpatterns = [
    path('add-user-order/', add_user_order, name='add'),
    path('open-order/', user_open_order, name='open-order'),
    path('remove-order-detail/<detail_id>', remove_order_detail),
    # path('request', send_request, name='request'),
    # path('verify/<order_id>', verify, name='verify'),
]
