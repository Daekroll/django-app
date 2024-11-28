from django.contrib.sitemaps import Sitemap

from .models import Product


class ShopSitemap(Sitemap):
    def items(self):
        return Product.objects.filter(is_archive=False).order_by('pk')
