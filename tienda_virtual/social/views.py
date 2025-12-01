from django.shortcuts import render


def links(request):
    """Página 'Sobre nosotros' / enlaces sociales (placeholder)."""
    return render(request, "social/links.html")
