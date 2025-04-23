from django.contrib import admin
from database.models import Blog_User,Blogs,Followers,Post_Like,Categories,Comment

admin.site.register(Blog_User)
admin.site.register(Categories)
admin.site.register(Blogs)
admin.site.register(Followers)
admin.site.register(Post_Like)
admin.site.register(Comment)