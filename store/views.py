from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse

def home(request):
    trending_products = Product.objects.filter(trending=1)
    context = {'trending_products':trending_products}
    return render(request, "store/index.html",context)

def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, "store/collections.html", context)

def collectionsview(request, slug):
    if Category.objects.filter(slug=slug, status=0).exists():
        category = Category.objects.filter(slug=slug).first()
        products = Product.objects.filter(category=category)
        context = {'products': products, 'category_name': category}
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')

def Productview(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=0).exists():
        if Product.objects.filter(slug=prod_slug, status=0).exists():
            product = Product.objects.get(slug=prod_slug, status=0)
            context = {'product': product}
            return render(request, "store/products/view.html", context)
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        return redirect('collections')
    

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productList = list(products)

    return JsonResponse(productList, safe=False)   

def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
             return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__icontains=searchedterm).first()



            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                 messages.info(request,"No product matched your search")
                 return redirect(request.META.get('HTTP_REFERER'))


            


    return redirect(request.META.get('HTTP_REFERER'))

 

