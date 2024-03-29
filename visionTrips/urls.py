from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings
# from product.views import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include("product.urls"), name='product')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)