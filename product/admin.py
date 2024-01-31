from django.contrib import admin
from .models import Product, ProductInfo, ProductGallery, ProductReviews, ProductExclusion, ProductInclusions, Category, SubCategory

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['product_description']}
    list_display = ['product_description', 'category', 'subcategory', 'price', 'num_of_days']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


    
admin.site.register([ProductInfo, ProductGallery, ProductReviews, ProductExclusion, ProductInclusions, SubCategory])
