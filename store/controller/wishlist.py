from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from store.models import Product,Wishlist
from django.contrib.auth.decorators import login_required

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request,'store/wishlist.html', context)


def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                   return JsonResponse({'status': "Product Already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id = prod_id)
                    return JsonResponse({'status': "Product Added to wishlist"})
            else:
                return JsonResponse({'status': "No such product Found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Add this if you're testing from JS and CSRF isn't working
def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            try:
                wishlistitem = Wishlist.objects.get(user=request.user, product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status': "Product removed from wishlist"})
            except Wishlist.DoesNotExist:
                return JsonResponse({'status': "Product not found in wishlist"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')

