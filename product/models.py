from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from common.modules.fields import CaseInsensitiveCharField


# Create your models here.
class Category(models.Model):
    name = CaseInsensitiveCharField(max_length=255, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs),
    
    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    name = CaseInsensitiveCharField(max_length=255, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs),
    
    class Meta:
        verbose_name_plural = "Sub Categories"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product_description = models.CharField(max_length=300, unique=True)
    price = models.CharField(max_length=15)
    num_of_days = models.CharField(max_length=15)
    slug = models.SlugField()
    pic = models.ImageField(upload_to='images/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_description
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-date_added']

class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_info')
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Product Information"

    def __str__(self):
        return f"product information for ~ {self.product.product_description}".lower()
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_gallery')
    pic = models.ImageField()

    def __str__(self):
        return f"images of ~ {self.product.product_description}".lower()
    
    class Meta:
        verbose_name_plural = "Product gallery"


class ProductReviews(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    rating = models.PositiveIntegerField(
            validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(5, message="Rating must be at most 5.")
        ], blank=True, null=True
    )
    comment = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    save_info = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} | {self.rating} star review on ~ {self.product.product_description}".lower()
    

class ProductInclusions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_inclusion')
    text = models.TextField()

    class Meta:
        verbose_name_plural = "Product Inclusion"

    def __str__(self):
        return f"inclusions for ~ {self.product.product_description}"

class ProductExclusion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_exclusion')
    text = models.TextField()

    class Meta:
        verbose_name_plural = "Product Exclusion"


    def __str__(self):
        return f"Exclusions for ~ {self.product.product_description}"

