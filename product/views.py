from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, ProductInfo, ProductGallery, ProductReviews, ProductExclusion,\
      ProductInclusions, Category, SubCategory
from common.modules.serializers import ProductSerializer, ProductDetailSerializer, ProductInfoSerializer, \
    ProductGallerySerializer, ProductExclusionSerializer, ProductInclusionSerializer, ProductReviewsSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from common.modules.pagination import ProductPagination
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.db.models.functions import Cast
from django.db.models import IntegerField,  Case, When, Value

from rest_framework.decorators import api_view  
from rest_framework.reverse import reverse  

# Create your views here.
#todo: remember to work on sub categories view

@api_view(["GET"])  # new
def api_root(request, format=None):
    return Response(
        {
            "products": reverse("all-products", request=request, format=format),
            "product_information": reverse("product_info", request=request, format=format),
        }
    )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class SubCategoryListView(GenericAPIView):
#     serializer_class = 
    
class ProductListView(GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    queryset = Product.objects.all()

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        order_by = self.request.query_params.get('days', None)
        price_order = self.request.query_params.get('price_order', None)
        alphabetical_order = self.request.query_params.get('alphabetical_order', None)
    
        # base queryset
        queryset = Product.objects.all()

        # Applying filter
        if category:
            queryset = queryset.filter(category__name__iexact=category)

        # Applying ordering
        if order_by:
            queryset = queryset.annotate(num_days_int=Cast('num_of_days', IntegerField())).order_by('-num_days_int')

        if price_order:
            int_price = Case(
               When(price__regex=r'^\d+$', then=Cast('price', IntegerField())),
               default=Value(0),
               output_field=IntegerField()
            )
            queryset = queryset.annotate(int_price=int_price)
            if price_order.lower() == 'high':
                queryset = queryset.order_by('-int_price')
            else:
                queryset = queryset.order_by('int_price')

        if alphabetical_order:
            queryset = queryset.order_by('product_description') if alphabetical_order.lower() == 'asc' else queryset.order_by('-product_description')
        
        return queryset

    def get(self, request, format=None):
        all_products = self.get_queryset()
        page = self.paginate_queryset(all_products)
        if page is not None:
            p = page
        else:
            p = all_products
        serializer = ProductSerializer(p, many=True)
        data = {
            "data": serializer.data,
            "message": "Retrieved successfully"
        }
        return self.get_paginated_response(data) if page is not None else Response(data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            message = "invalid data"
            return Response(message) 
       
class ProductDetailView(GenericAPIView):
    serializer_class = ProductDetailSerializer

    def get_object(self, slug):
        return get_object_or_404(Product, slug=slug)
    
    def get(self, request, slug, format=None):
        product = self.get_object(slug)
        serializer = self.serializer_class(product)

        data = {
            "data": serializer.data,
            "message": "Retrieved successfully"
        }
        return Response(data)
        
class ProductInfoListView(GenericAPIView):
    serializer_class = ProductInfoSerializer

    def get_queryset(self, slug):
        return ProductInfo.objects.filter(product__slug=slug)

    def get(self, request, slug, format=None):
        product_info = self.get_queryset(slug)

        if product_info.exists(): 
            serializer = self.serializer_class(product_info, many=True)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            message = 'No product information found for the specified product slug.'
            return Response({"message": message}, status=404)
        
    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        product_info = ProductInfo.objects.filter(product__slug=slug)
        if product_info.exists():
           message = {
               "message":'Only PUT requests are allowed because an item already exists.'}
           return Response(message)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                message = "Comment successfully added !"
                context = {
                    'data': serializer.data,
                    'message': message
                }
                return Response(context, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class ProductInfoDetailView(GenericAPIView):
    serializer_class = ProductInfoSerializer

    def get_queryset(self, slug):
        return ProductInfo.objects.filter(product__slug=slug)
    
    def get(self, request, pk, slug, format=None):
        product_info = self.get_queryset(slug).filter(pk=pk).first()
        if product_info:
            serializer = self.serializer_class(product_info)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def put(self, request, pk, slug, format=None):
        product_info = self.get_queryset(slug).filter(pk=pk).first()
        if product_info:
            serializer = self.serializer_class(product_info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data":serializer.data,
                    "message": "Updated successfully "
                }
                return Response(data)
            else:
                data = {
                    "message": "invalid data"
                }
                return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def delete(self, request, pk, slug, format=None):
        product_info = self.get_queryset(slug).filter(pk=pk).first()
        if product_info:
            product_info.delete()
            data = {
                "message": "DELETED !"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
class ProductGalleryListView(GenericAPIView):
    serializer_class = ProductGallerySerializer

    def get_queryset(self, slug):
        return ProductGallery.objects.filter(product__slug=slug)
            
    def get(self, request, slug, format=None):
        product_gallery = self.get_queryset(slug)

        if product_gallery.exists():
            serializer = self.serializer_class(product_gallery, many=True)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            message = 'No gallery found for the specified product slug.'
            return Response({"message": message}, status=404)
        
    
    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            message = "Picture successfully added !"
            data = {
                    'data': serializer.data,
                    'message': message
                }
            return Response(data)
        else:
            data = {
                "message": "Invalid data"
            }
            return Response(data)
        
class ProductGalleryDetailView(GenericAPIView):
    serializer_class = ProductGallerySerializer

    def get_queryset(self, slug):
        return ProductGallery.objects.filter(product__slug=slug)
    
    def get(self, request, pk, slug, format=None):
        product_gallery = self.get_queryset(slug).filter(pk=pk).first()
        if product_gallery:
            serializer = self.serializer_class(product_gallery)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def put(self, request, pk, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        product_gallery = self.get_queryset(slug).filter(pk=pk).first()
        if product_gallery:
            serializer = self.serializer_class(product_gallery, data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                data = {
                    "data":serializer.data,
                    "message": "Updated successfully "
                }
                return Response(data)
            else:
                data = {
                    "message": "invalid data"
                }
                return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def delete(self, request, pk, slug, format=None):
        product_gallery = self.get_queryset(slug).filter(pk=pk).first()
        if product_gallery:
            product_gallery.delete()
            data = {
                "message": "DELETED !"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)

class ProductExclusionListView(GenericAPIView):
    serializer_class = ProductExclusionSerializer

    def get_queryset(self, slug):
        return ProductExclusion.objects.filter(product__slug=slug)
            
    def get(self, request, slug, format=None):
        product_exclusion = self.get_queryset(slug)

        if product_exclusion.exists():
            serializer = self.serializer_class(product_exclusion, many=True)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            message = 'No exclusion found for the specified product slug.'
            return Response({"message": message}, status=404)
        
    
    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        product_exclusion = self.get_queryset(slug)
        if product_exclusion.exists():
           message = {
               "message":'Only PUT requests are allowed because an item already exists.'}
           return Response(message)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            message = "successfully added !"
            data = {
                    'data': serializer.data,
                    'message': message
                }
            return Response(data)
        else:
            data = {
                "message": "Invalid data"
            }
            return Response(data)
        
class ProductExclusionDetailView(GenericAPIView):
    serializer_class = ProductExclusionSerializer

    def get_queryset(self, slug):
        return ProductExclusion.objects.filter(product__slug=slug)
    
    def get(self, request, pk, slug, format=None):
        product_exclusion = self.get_queryset(slug).filter(pk=pk).first()
        if product_exclusion:
            serializer = self.serializer_class(product_exclusion)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def put(self, request, pk, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        product_exclusion = self.get_queryset(slug).filter(pk=pk).first()
        if product_exclusion:
            serializer = self.serializer_class(product_exclusion, data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                data = {
                    "data":serializer.data,
                    "message": "Updated successfully "
                }
                return Response(data)
            else:
                data = {
                    "message": "invalid data"
                }
                return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def delete(self, request, pk, slug, format=None):
        product_exclusion = self.get_queryset(slug).filter(pk=pk).first()
        if product_exclusion:
            product_exclusion.delete()
            data = {
                "message": "DELETED !"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
    
class ProductInclusionListView(GenericAPIView):
    serializer_class = ProductInclusionSerializer

    def get_queryset(self, slug):
        return ProductInclusions.objects.filter(product__slug=slug)
            
    def get(self, request, slug, format=None):
        product_inclusion = self.get_queryset(slug)

        if product_inclusion.exists():
            serializer = self.serializer_class(product_inclusion, many=True)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            message = 'No exclusion found for the specified product slug.'
            return Response({"message": message}, status=404)
        
    
    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        product_inclusion = self.get_queryset(slug)
        if product_inclusion.exists():
           message = {
               "message":'Only PUT requests are allowed because an item already exists.'}
           return Response(message)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            message = "successfully added !"
            data = {
                    'data': serializer.data,
                    'message': message
                }
            return Response(data)
        else:
            data = {
                "message": "Invalid data"
            }
            return Response(data)
        
class ProductInclusionDetailView(GenericAPIView):
    serializer_class = ProductInclusionSerializer

    def get_queryset(self, slug):
        return ProductInclusions.objects.filter(product__slug=slug)
    
    def get(self, request, pk, slug, format=None):
        product_inclusion = self.get_queryset(slug).filter(pk=pk).first()
        if product_inclusion:
            serializer = self.serializer_class(product_inclusion)
            data = {
                "data": serializer.data,
                "message": "Retrieved successfully"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def put(self, request, pk, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        product_inclusion = self.get_queryset(slug).filter(pk=pk).first()
        if product_inclusion:
            serializer = self.serializer_class(product_inclusion, data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                data = {
                    "data":serializer.data,
                    "message": "Updated successfully "
                }
                return Response(data)
            else:
                data = {
                    "message": "invalid data"
                }
                return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
        
    def delete(self, request, pk, slug, format=None):
        product_inclusion = self.get_queryset(slug).filter(pk=pk).first()
        if product_inclusion:
            product_inclusion.delete()
            data = {
                "message": "DELETED !"
            }
            return Response(data)
        else:
            data = {
                "message": "No item exists at this id"
            }
            return Response(data)
    
class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewsSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return ProductReviews.objects.filter(product__slug=slug)

    @action(detail=True, methods=['post'])
    def add_rating_and_comment(self, request, slug):
        review = get_object_or_404(self.get_queryset(), product__slug=slug)
        if 'rating' not in request.data:
            return Response({'error': "Rating is required."}, status=404)
        
        rating = int(request.data['rating'])

        if not 1 <= rating <=5:
            return Response({'error': 'Invalid rating. Must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        review.rating = rating
        review.comment = request.data.get('comment', '')
        review.name = request.data.get('name', '')
        review.email = request.data.get('email', '')
        review.website = request.data.get('website', '')
        review.save_info = request.data.get('save_info', False)

        try:
            review.full_clean()  # Validate all model fields, including validators
            review.save()
            serializer = self.serializer_class(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
