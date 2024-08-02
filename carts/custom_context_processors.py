from .models import Cart


def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return {'cart_counter': cart.cart_items.count()}
