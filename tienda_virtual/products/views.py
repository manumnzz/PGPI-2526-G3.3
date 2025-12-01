from django.shortcuts import render


def product_list(request):
    """Vista placeholder de listado de productos."""
    return render(request, "products/list.html")
