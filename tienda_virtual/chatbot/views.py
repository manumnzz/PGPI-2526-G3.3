from django.shortcuts import render


def index(request):
    """Vista placeholder para chatbot."""
    return render(request, "chatbot/index.html")
