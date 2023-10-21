from django.urls import path

from .views import HomeTemplateView, ProductTemplateView


app_name = "products"
urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("products/", ProductTemplateView.as_view(), name="home"),
]
