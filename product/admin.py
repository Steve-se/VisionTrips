from django.contrib import admin
from .models import Product, ProductInfo, ProductGallery, ProductReviews, ProductExclusion, ProductInclusions, Category, SubCategory

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['product_description']}
    
admin.site.register([ProductInfo, ProductGallery, ProductReviews, ProductExclusion, ProductInclusions, Category, SubCategory])
