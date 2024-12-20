"""
URL configuration for bali_heritage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Homepage.urls')),
    path('stories/', include('BaliLoka_stories.urls')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('review/',include('Review.urls')),
    path('bookmarks/', include('bookmarks.urls')),
    path('auth/', include('authentication.urls')),  # Include the authentication URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
