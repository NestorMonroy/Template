from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product

# Create your views here.
class ProductListView(ListView):
    template_name = "products/list.html"


    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     context['cart'] = cart_obj
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # print( Product.objects.all())
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list' : queryset
    }
    # print('n')
    return render(request, "products/list.html", context)
