from django.urls import path
from .views import CategoriesView, ProductIdView, ProductIdReviewView, TagView, CatalogView

urlpatterns = [
    path("categories", CategoriesView.as_view(), name="categories"),
    path("product/<int:id>", ProductIdView.as_view(), name="product"),
    path("product/<int:id>/reviews", ProductIdReviewView.as_view(), name="review"),
    path("tags", TagView.as_view(), name="tag"),
    path("catalog", CatalogView.as_view(), name="catalog"),
]
