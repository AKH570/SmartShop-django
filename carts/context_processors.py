from .models import Cart, Cartitem
from .views import _cart_id
from django.http import HttpResponse


def counter(request):
    cart_count = 0
    """
    if 'admin' in request.path:   # It checks that the requested user is an admin or not
        return {}
    else:
    """
    try:
        cart = Cart.objects.filter(cart_id = _cart_id(request))
        cart_items = Cartitem.objects.all().filter(carts = cart[:1])
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
    return HttpResponse(cart_count, 'cart.html')
