from django.urls import path
from .views import (
    CategoriesView,
    ProductIdView,
    ProductIdReviewView,
    TagView,
    CatalogView,
    ProductPopularView,
    ProductLimitedView,
    BannerView,
    SaleView
)

urlpatterns = [
    path("categories", CategoriesView.as_view(), name="categories"),
    path("product/<int:id>", ProductIdView.as_view(), name="product"),
    path("product/<int:id>/reviews", ProductIdReviewView.as_view(), name="review"),
    path("products/popular", ProductPopularView.as_view(), name="products-popular"),
    path("products/limited", ProductLimitedView.as_view(), name="products-limited"),
    path("tags", TagView.as_view(), name="tag"),
    path("catalog", CatalogView.as_view(), name="catalog"),
    path("banners", BannerView.as_view(), name="banners"),
    path("sales", SaleView.as_view(), name="sales")
]
