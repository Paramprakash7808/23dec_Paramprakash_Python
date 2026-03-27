from django.contrib import admin
from django.urls import path, include

from django.http import HttpResponse

def home(request):
    html = """
    <h1>Django Project: Doctor Admin & Paytm Integration</h1>
    <ul>
        <li><a href="/admin/">Django Admin (Doctor Customization)</a></li>
        <li><a href="/payments/pay/">Paytm Payment Gateway Demo</a></li>
    </ul>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('payments/', include('payments.urls')),
]
