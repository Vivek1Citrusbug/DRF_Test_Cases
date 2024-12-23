from django.shortcuts import render

def home_page(request):
    """This view is used for redirecting user to home page"""

    return render(request,'accounts/index.html')