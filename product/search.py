from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from common.modules.serializers import ProductSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def product_search(request):

    items_per_page = 10
    page_number =  request.query_params.get('page', 1)
    query = None
    results = []

    # Use request.GET instead of request.data for query parameters
    if 'query' in request.GET:
        query = request.GET['query']
        # Annotate and filter the queryset for search
        search_vector = SearchVector('category', 'subcategory', 'product_description', 'price', 'num_of_days')
        search_query = SearchQuery(query)
        results = Product.objects.annotate(
            search = search_vector,
            rank = SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('rank')

        paginator = Paginator(results, items_per_page)

        try:
            current_page = paginator.page(page_number)
        except PageNotAnInteger:
            # if page is not an integer,deliver the first page
            current_page = paginator.page(1)
        except EmptyPage:
            #  if page is out of range, deliver the last page of the result
            current_page = Paginator.page(paginator.num_pages)

        serializer = ProductSerializer(current_page, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': current_page.number,
            'next_page': current_page.next_page_number() if current_page.has_next() else None,
            'previous_page': current_page.previous_page_number() if current_page.has_previous() else None,
            'results': serializer.data
        })
    else:
        return Response({
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': current_page.number,
                'next_page': current_page.next_page_number() if current_page.has_next() else None,
                'previous_page': current_page.previous_page_number() if current_page.has_previous() else None,
                'results': serializer.data
            })
            



