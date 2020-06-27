from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from .models import Product

# class ProductList(ListView):
#     model = Product
#     paginate_by = 8
#     template_name = "products/list.html"

class ProductList(View):

    def get(self, *args, **kwargs):
        object_list = Product.objects.all()
        category = self.request.GET.get('category', '')
        if category:
            object_list = object_list.filter(
                category=category
            )
        search_term = self.request.GET.get('search_term', '')
        if search_term:
            object_list = object_list.filter(
                title__icontains=search_term
            )
        paginator = Paginator(object_list, 8)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'products/list.html', {'page_obj': page_obj})