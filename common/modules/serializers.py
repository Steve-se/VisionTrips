from product.models import Product, ProductInfo, ProductGallery, ProductReviews, ProductExclusion, ProductInclusions, Category, SubCategory
from rest_framework import serializers
from markdown import markdown as md


#todo: remember to fix the markdown bug (The field boxes are not showing in the browsable api)
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_category']

class ProductInfoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    class Meta:
        model = ProductInfo
        fields = "__all__"

    def get_product(self, obj):
        return obj.product.product_description
    
    def get_description(self, obj):
        a = obj.description if hasattr(obj, "description") else None
        return md(a) if a else None


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = "__all__"

class ProductReviewsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField
    class Meta:
        model = ProductReviews
        fields = "__all__"

    def get_product(self, obj):
        return obj.product.product_description

class ProductExclusionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    class Meta:
        model = ProductExclusion
        fields = "__all__"
    
    def get_text(self, obj):
        return md(obj.text)
    
class ProductInclusionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    class Meta:
        model = ProductInclusions
        fields = ['product', 'text']

    def get_text(self, obj):
       a = obj.text if hasattr(obj, "text") else None
       return md(a) if a else None


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        exclude = ['date_added']

class ProductDetailSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(many=True,read_only=True)
    product_gallery = ProductGallerySerializer(many=True, read_only=True)
    product_review = ProductReviewsSerializer(many=True, read_only=True)
    product_exclusion = ProductExclusionSerializer(many=True, read_only=True)
    product_inclusion = ProductInclusionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        exclude = ['price', 'num_of_days', 'slug', 'pic' ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
    
        # Check if there is at least one related ProductInfo
        if 'product_info' in data and not instance.product_info.exists():
            data.pop('product_info')

        if 'product_gallery' in data and not instance.product_gallery.exists():
            data.pop('product_gallery')

        if 'product_review' in data and not instance.product_review.exists():
            data.pop('product_review')

        if 'product_exclusion' in data and not instance.product_exclusion.exists():
            data.pop('product_exclusion')
        
        if 'product_inclusion' in data and not instance.product_inclusion.exists():
            data.pop('product_inclusion')
 
        return data

       
