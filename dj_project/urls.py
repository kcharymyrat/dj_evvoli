from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path("admin/", admin.site.urls),
] + i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("products.urls", namespace="products")),
    path("", include("orders.urls", namespace="orders")),
    path("api/", include("api.urls", namespace="api")),
    path("__debug__/", include("debug_toolbar.urls")),  # only when testing
    prefix_default_language=False,
)

# handler404 = "products.views.my_custom_page_not_found_view"

# print(type(settings))
if settings.DEBUG:
    # urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
