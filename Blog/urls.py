"""
URL configuration for Blog project.

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
from . import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import *
from .views import custom_page_not_found
from django.conf.urls import handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home,name="Home"),
    path('blogs', Blogs,name="Blogs"),
    path('blogs/catogory/<str:catogory>', Catogories,name="Catogories"),
    path('profile/<str:username>',Profile,name="Profile"),
    path('profile',Profile,name="Profile_user"),
    path('login',Login,name="Login"),
    path('signup',SignUp,name="Sign Up"),
    path('blogs/create',CreateBlog,name="Create Blog"),
    path('blogs/<slug:slug>',BlogDetails,name="Blog_Details"),
    path('signout',SignOut,name="Sign Out"),
    path('search/blogs',BlogSearch,name="Blog Search"),
    path("follow/<str:username>",Follow,name="Follow"),
    path("unfollow/<str:username>",Unfollow,name="Unfollow"),
    path("like/<slug:slug>",like_Post,name="Like Post"),
    path("blogs/delete/<slug:slug>",Delete_Blog,name="Delete_Blog"),
    path("blogs/edit/<slug:slug>",Edit_Blog, name="Edit Blog"),
    path("upload/profile",upload_profile_img,name="Upload Profile Image"),
    path("comment/<slug:slug>",add_comment,name="Comment"),

    
    path("__reload__/", include("django_browser_reload.urls")),
    
     
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
