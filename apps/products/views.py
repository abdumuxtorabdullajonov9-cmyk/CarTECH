from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Mahsulot


def product_list_view(request):
    search_query = request.GET.get('q', '')

    if search_query:
        products = Mahsulot.objects.filter(
            Q(nomi__icontains=search_query) | Q(artikul_raqami__icontains=search_query),
            faol=True
        )
    else:
        products = Mahsulot.objects.filter(faol=True)

    context = {
        'products': products,
        'search_query': search_query
    }
    return render(request, 'products/products_list.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Mahsulot, slug=slug, faol=True)

    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)
