from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product,Variation
from .models import Cart, Cartitem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            #print(key)
            try:
                variation = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    #return HttpResponse(color)
    #exit()

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    is_cart_item_exists = Cartitem.objects.filter(product=product,carts=cart).exists() #exists() return boolean data
    print(is_cart_item_exists)
    if is_cart_item_exists:
        cart_item = Cartitem.objects.filter(product=product, carts=cart)
         #existing variations->database
        # current variations->product_variation
        #item id -> database
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
        print(ex_var_list)
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = Cartitem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
            #return HttpResponse('True')
        else:
            #return HttpResponse('False')
            if len(product_variation) >0:
                cart_item.variations.clear()
                for item in product_variation:
                    cart_item.variations.add(item)
       # cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item = Cartitem.objects.create(
            product=product,
            quantity=1,
            carts=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cartitem.objects.get(product=product, carts=cart)
    if cart_item.quantity > 1:
       cart_item.quantity -= 1
       cart_item.save()
    else:
       cart_item.delete()
    return redirect( 'cart' )

def remove_cart_item(request, product_id):
    cart = Cart.objects.get( cart_id=_cart_id( request ) )
    product = get_object_or_404( Product, id=product_id )
    cart_item = Cartitem.objects.get( product=product, carts=cart )
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_item=None):
    grand_total = 0
    cart_items = 0
    tax = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(carts=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
