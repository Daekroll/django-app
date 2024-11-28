from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import shop_index, product_list_view, order_view, create_product, new_order, ProductListView, \
    ProductDetailView, ProductUpdateView, ProductDeleteView, ProductCreateView, OrderListView, OrderDetailView, \
    OrderUpdateView, OrderDeleteView, order_list_json_view, ProductApiViewSet, OrderApiViewSet, LatestProductsFeed, \
    UserOrdersListView, UserOrderJSONView

app_name = 'shopapp'

router = DefaultRouter()
router.register("products", ProductApiViewSet)
router.register("orders", OrderApiViewSet)

urlpatterns = [
    path("", shop_index, name="index"),
    # path('product_list/', product_list_view, name='product_list'),
    # path('order_list/', order_view, name='order_list'),
    # path('create_product/', new_product, name='create_product'),
    path('create_order/', new_order, name='create_order'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_list/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_list/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product_list/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_archive'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),

    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order_detail/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order_detail/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('user/<int:pk>/orders/', UserOrdersListView.as_view(), name='user_order'),
    path('user/<int:pk>/orders/export/', UserOrderJSONView.as_view(), name='user_orders_export'),

    path('orders_json/', order_list_json_view, name='orders_json'),

    path('api/', include(router.urls)),
    path("product/latest/feed/", LatestProductsFeed(), name='product-feed'),
]
