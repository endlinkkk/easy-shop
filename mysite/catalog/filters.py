from distutils.util import strtobool
from .models import Product
from django.http import HttpRequest
from django.db.models import Q

def products_filter(request: HttpRequest) -> list[Product]:
    d = {"inc": "-", "dec": ""}
    name = request.GET.get("filter[name]")
    min_price = request.GET.get("filter[minPrice]")
    max_price = request.GET.get("filter[maxPrice]")
    free_delivery = request.GET.get("filter[freeDelivery]")
    available = request.GET.get("filter[available]")
    sort = request.GET.get("sort")
    sort_type = request.GET.get("sortType")
    limit = request.GET.get("limit")
    products = Product.objects.all().order_by(f"{d[sort_type]}{sort}")

    if available == "true":
        avail_filter = Q(count__gt=0)
    elif available == "false":
        avail_filter = Q(count__lte=0)

    if name:
        name_filter = Q(title__icontains=name)
    else:
        name_filter = Q()

    products = products.filter(
        Q(price__gte=min_price),
        Q(price__lte=max_price),
        Q(freeDelivery=strtobool(free_delivery)),
        avail_filter,
        name_filter,
    )
    return products