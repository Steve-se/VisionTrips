from django.urls import path, include
from .views import  ProductListView, ProductDetailView, ProductInfoListView, ProductInfoDetailView, ProductGalleryListView, \
ProductGalleryDetailView, ProductExclusionListView, ProductExclusionDetailView, ProductInclusionListView, ProductInclusionDetailView,\
      ProductReviewViewSet, CategoryViewSet, api_root
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products/<slug:slug>/product-reviews', ProductReviewViewSet, basename='product-review')
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'sub-categories/', SubCategoryViewSet, basename='sub-categories')

app_name = "product"

urlpatterns = [ 
    path('products/', ProductListView.as_view(), name='all-products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='single_product'),
    path('products/<slug:slug>/product-info/', ProductInfoListView.as_view(), name='product_info'),
    path('products/<slug:slug>/product-info/<str:pk>/', ProductInfoDetailView.as_view(), name='product_info_detail'),
    path('products/<slug:slug>/product-gallery/', ProductGalleryListView.as_view(), name='product_gallery'),
    path('products/<slug:slug>/product-gallery/<str:pk>/', ProductGalleryDetailView.as_view(), name='product_gallery'),
    path('products/<slug:slug>/product-exclusion/', ProductExclusionListView.as_view(), name='product_exclusion'), 
    path('products/<slug:slug>/product-exclusion/<str:pk>', ProductExclusionDetailView.as_view(), name='product_exclusion'), 
    path('products/<slug:slug>/product-inclusion/', ProductInclusionListView.as_view(), name='product_inclusion'), 
    path('products/<slug:slug>/product-inclusion/<str:pk>/', ProductInclusionDetailView.as_view(), name='product_inclusion'), 
    path('', include(router.urls)),
    path('home/', api_root, name='home')
    
]