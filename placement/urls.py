from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("planning/", views.planning, name="planning"),
    path("monitoring/", views.monitoring, name="monitoring"),
    path("maintenance/", views.maintenance, name="maintenance"),
    path("history/", views.history, name="history"),
    path("report/", views.report, name="report"),
]



path("media/<path:path>", serve, {
    "document_root": settings.MEDIA_ROOT
}),