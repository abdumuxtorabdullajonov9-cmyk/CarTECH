from django.shortcuts import render, redirect, get_object_or_404
from apps.products.models import Mahsulot


def cart_add(request, product_id):
    product = get_object_or_404(Mahsulot, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str not in cart:
        cart[product_id_str] = {
            'id': product.id,
            'quantity': 1,
            'narxi': int(product.narxi),
            'nomi': product.nomi,
            'artikul': product.artikul_raqami,
            'rasm_url': product.rasm.url if product.rasm else None
        }
    else:
        cart[product_id_str]['quantity'] += 1

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('cart_detail')


def cart_decrement(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1
        else:
            del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('cart_detail')


def cart_clear(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})

    total_price = sum(int(item.get('narxi', 0)) * item.get('quantity', 0) for item in cart.values())

    for item in cart.values():
        item['jami_narxi'] = int(item.get('narxi', 0)) * item.get('quantity', 0)

    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total_price': total_price})
