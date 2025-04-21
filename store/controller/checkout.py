
from django.shortcuts import render, redirect
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from store.models import Cart, Order,OrderItem,Product,Profile
from django.contrib.auth.models import User

import random


@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)

    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0

    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()    


    context={'cartitems':cartitems, 'total_price':total_price, 'userprofile':userprofile}
    return render(request, "store/checkout.html",context)

@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()

        neworder = Order()  # ✅ Create neworder early so it's accessible

        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.pincode = request.POST.get('pincode')
        neworder.user = request.user

        # ✅ Assign current user names AFTER neworder is defined
        if not currentuser.first_name:
            currentuser.first_name = neworder.fname
            currentuser.last_name = neworder.lname
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)

        cart_total_price = 0
        for item in cart:
            cart_total_price += item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price

        trackno = 'naveen' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():  # ✅ corrected the check
            trackno = 'naveen' + str(random.randint(1111111, 9999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed successfully")

    return redirect('/')

@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0

    for item in cart:
        total_price = total_price + item.product.selling_price * item.product_qty


        return JsonResponse({
            'total_price': total_price
        })
    