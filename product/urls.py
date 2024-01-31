from django.urls import path, include
from .views import  ProductListView, ProductDetailView, ProductInfoListView, ProductInfoDetailView,  \
ProductGalleryDetailView, ProductExclusionListView, ProductExclusionDetailView, ProductInclusionListView, \
    ProductInclusionDetailView,  ProductReviewViewSet, CategoryListView, ProductGalleryListView, CategoryDetailView,\
    SubCategoryListView, SubCategoryDetailView

from .search import product_search
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', ProductReviewViewSet, basename='product-review')

app_name = "product"

urlpatterns = [ 
    path('products/', ProductListView.as_view(), name='all-products'),
    path('products/search/', product_search, name='search_product'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='single_product'),
    path('products/<slug:slug>/product-info/', ProductInfoListView.as_view(), name='product_info'),
    path('products/<slug:slug>/product-info/<str:pk>/', ProductInfoDetailView.as_view(), name='product_info_detail'),
    path('products/<slug:slug>/product-gallery/', ProductGalleryListView.as_view(), name='product_gallery'),
    path('products/<slug:slug>/product-gallery/<str:pk>/', ProductGalleryDetailView.as_view(), name='product_gallery'),
    path('products/<slug:slug>/product-exclusion/', ProductExclusionListView.as_view(), name='product_exclusion'), 
    path('products/<slug:slug>/product-exclusion/<str:pk>/', ProductExclusionDetailView.as_view(), name='product_exclusion'), 
    path('products/<slug:slug>/product-inclusion/', ProductInclusionListView.as_view(), name='product_inclusion'), 
    path('products/<slug:slug>/product-inclusion/<str:pk>/', ProductInclusionDetailView.as_view(), name='product_inclusion'), 
    path('products/<slug:slug>/product-reviews/', include(router.urls)),
    path('category/', CategoryListView.as_view(), name='all_categories'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('category/<slug:slug>/subcategory/', SubCategoryListView.as_view(), name='all_sub_category'),
    path('category/<slug:slug>/subcategory/<str:pk>/', SubCategoryDetailView.as_view(), name='all_sub_category'),
]