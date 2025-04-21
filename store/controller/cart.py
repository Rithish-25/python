from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from store.models import Product, Cart

from django.contrib.auth.decorators import login_required


def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            prod_qty = request.POST.get('product_qty')

            if not prod_id or not prod_id.isdigit():
                return JsonResponse({'status': "Invalid product ID"})

            prod_id = int(prod_id)

            try:
                product_check = Product.objects.get(id=prod_id)

                if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
                    return JsonResponse({'status': "Product already in cart"})

                if not prod_qty or not prod_qty.isdigit():
                    return JsonResponse({'status': "Invalid quantity"})

                prod_qty = int(prod_qty)

                if product_check.quantity >= prod_qty:
                    Cart.objects.create(
                        user=request.user,
                        product=product_check,
                        product_qty=prod_qty
                    )
                    return JsonResponse({'status': "Product added successfully"})
                else:
                    return JsonResponse({'status': f"Only {product_check.quantity} quantity available"})

            except Product.DoesNotExist:
                return JsonResponse({'status': "No such product found"})

        else:
            return JsonResponse({'status': "Login to continue"})

    return redirect('/')

@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request, "store/cart.html", context)


def upadtecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id =prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"updated successfully"})
    return redirect('/')

def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"deleted successfully"})
    return redirect('/')

        

