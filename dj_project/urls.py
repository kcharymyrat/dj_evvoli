from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog

from products.views import (
    PageNotFoundView,
    BadRequestView,
    ForbiddenView,
    ServerErrorView,
    PageNotFoundView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
] + i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("products.urls", namespace="products")),
    path("", include("orders.urls", namespace="orders")),
    path("api/", include("api.urls", namespace="api")),
    prefix_default_language=False,
)

handler404 = PageNotFoundView.as_view()
handler400 = BadRequestView.as_view()
handler403 = ForbiddenView.as_view()
handler404 = PageNotFoundView.as_view()
handler500 = ServerErrorView.as_view()


if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
