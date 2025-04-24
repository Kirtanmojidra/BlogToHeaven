from django.shortcuts import render,redirect
from django.utils.text import slugify
from database.models import Blog_User,Followers,Post_Like,Categories,Comment
from database.models import Blogs as Blog
from django.db import IntegrityError
from .components.Auth.JWT import encode,decode
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import JsonResponse
from django.core.paginator import Paginator
import random,string
from .forms import BlogPostForm
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json


def custom_page_not_found(request,exception):
    return render(request, '404.html', status=404)
def generate_custom_filename(extension):
    """
    Generate a custom filename using a random string and timestamp.
    """
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f'{random_string}.{extension}'

def validateToken(token):
    try:
        username = decode(token)
        user = Blog_User.objects.get(username=username['username'])
        return user
    except Exception as e:
        print(e)
        return False

@csrf_exempt
def Home(request):
    blogs = Blog.objects.all().order_by('-created_At')  
    Auth_token = request.COOKIES.get("Auth_token")
    try:
        categories = Categories.objects.all()
    except Exception as e:
        categories = ""
    if Auth_token is not None:
        Auth_user = validateToken(Auth_token)
        if Auth_user:
            return render(request, 'home/index.html',{"categories":categories,"blogs":blogs,"Auth_user":Auth_user,"user":{"IsLoggedIn":True}})
        else:
            return render(request, 'home/index.html',{"categories":categories,"blogs":blogs,"user":{"IsLoggedIn":False}})
    else:
        return render(request, 'home/index.html',{"categories":categories,"blogs":blogs,"user":{"IsLoggedIn":False}})
@csrf_exempt
def Blogs(request):
    blogs = Blog.objects.all().order_by('-created_At')
    Auth_token = request.COOKIES.get("Auth_token")
    try:
        categories = Categories.objects.all()
    except Exception as e:
        categories = ""
    if Auth_token is not None:
        Auth_user = validateToken(Auth_token)
        if Auth_user:
            return render(request, 'blogs/index.html',{"categories":categories,"blogs":blogs,"Auth_user":Auth_user})
        else:
            return render(request, 'blogs/index.html',{"categories":categories,"blogs":blogs,"user":{"IsLoggedIn":False}})
    else:
        return render(request, 'blogs/index.html',{"categories":categories,"blogs":blogs,"user":{"IsLoggedIn":False}})
@csrf_exempt
def Catogories(request,catogory):
    Auth_token  = request.COOKIES.get("Auth_token")
    try:
        categories = Categories.objects.all()
        catogory = Categories.objects.get(name=catogory)
        print(catogory.image)
    except Exception as e:
        categories = ""
    try:
        blogs = Blog.objects.filter(categories__name=catogory).order_by('-created_At')
    except Exception as e:
        blogs = ""
        print(e)
        return render(request, 'blogs/catogories.html',{"categories":categories,"catogory":catogory,'Auth_user':user,"message":"No Blog Found For This Catogory","user":{"IsLoggedIn":False}})
    if Auth_token:
        user = validateToken(Auth_token)
        if user:
            if not blogs:
                return render(request, 'blogs/catogories.html',{"categories":categories,"catogory":catogory,'Auth_user':user,"message":"No Blog Found For This Catogory","user":{"IsLoggedIn":False}})
            return render(request, 'blogs/catogories.html',{"categories":categories,"blogs":blogs,"catogory":catogory,'Auth_user':user,"user":{"IsLoggedIn":True,"username":user.username}})
        else:
            if blogs:
                return render(request, 'blogs/catogories.html',{"categories":categories,"catogory":catogory,"blogs":blogs, "user":{"IsLoggedIn":False}})
            else:
                return render(request, 'blogs/catogories.html',{"categories":categories,"catogory":catogory,'Auth_user':user,"message":"No Blog Found For This Catogory","user":{"IsLoggedIn":False}})
    else:
        if blogs:
            return render(request, 'blogs/catogories.html',{"categories":categories,"catogory":catogory,"blogs":blogs,})
        else:
            return render(request, 'blogs/catogories.html',{"categories":categories,"catogory":catogory,"message":"No Blog Found For This Catogory",})

@csrf_exempt
def Profile(request,username):
    Auth_token = request.COOKIES.get("Auth_token")
    try:
        categories = Categories.objects.all()
    except Exception as e:
        catogories = ""
    if Auth_token is not None:
        Auth_user = validateToken(Auth_token)
        try:
            user = Blog_User.objects.get(username=username)
        except Exception as e:
            print(e)
            return render(request,'404.html',{"categories":categories},status=404)
        if Auth_user:
            try:
                if user:
                    if Auth_user != user:
                        try:
                            is_following = Followers.objects.filter(follower=Auth_user,following=user).exists()
                        except Exception as e:
                            print(e)
                            is_following = False
                    else:
                        is_following = False
                blogs = Blog.objects.filter(author=user)
                if blogs:
                    print(blogs[0].author.username)
                    return render(request, 'profile.html',{"categories":categories,"blogs":blogs,"Auth_user":Auth_user,"Is_following":is_following,"user":user})
                else:
                    pass
                return render(request, 'profile.html',{"categories":categories,"Auth_user":Auth_user,"user":user,"Is_following":is_following,})
            except Exception as e:
                print(e)
            return render(request, 'profile.html',{"categories":categories,"user":user,"Is_following":is_following,})
        else:
            user = Blog_User.objects.get(username=username)
        if user:
            return render(request, 'profile.html',{"categories":categories,"user":user})
    else:
        user = Blog_User.objects.get(username=username)
        if user:
            return render(request, 'profile.html',{"categories":categories,"user":user})
        else:
            return render(request,'404.html',status=404)
@csrf_exempt
def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username is None or password is None:
            return render(request, 'auth/login.html',{"error":"All fields are required"})
        else:
            try:
                user = Blog_User.objects.get(username=username,password=password)
                Auth_token = encode(data={"username":username})
                if user:
                    responce = redirect(f"/profile/{user.username}") 
                    responce.set_cookie("Auth_token",Auth_token,expires=24*60*60)
                    return responce
                else:
                    print("Error while fetching user")
                    return render(request, 'auth/login.html',{"error":"Please Try Again Later"})
            except Exception as e:
                print(e)
                return render(request, 'auth/login.html',{"error":"Invalid Username or Password"})
    else:
        if request.COOKIES.get("Auth_token"):
            Auth_token = request.COOKIES.get("Auth_token")
            user = validateToken(Auth_token)
            if user:
                print("user Found")
                return redirect(f"profile/{user.username}")
        return render(request, 'auth/login.html',{"user":{"IsLoggedIn":True}})

@csrf_exempt
def SignUp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("confirm_password")
        print(username,email,password,password2)
        if username is None or email is None or password is None or password2 is None:
            return render(request, 'auth/signup.html',{"error":"All fields are required"})
        else:
            if password != password2:
                return render(request, 'auth/signup.html',{"error":"Password and Confirm Password doesn't match"})
            else:
                try:
                    user = Blog_User(username=username,email=email,password=password)
                    try:
                        user.save()
                        responce = redirect("/login")
                        return responce
                    except IntegrityError as e:
                        print(e)
                        return render(request, 'auth/signup.html',{"error":"Username or Email is Already Taken"})
                except Exception as e:
                    print(e)
                    return render(request, 'auth/signup.html',{"error":"Try Again Later"})
    else:
        return render(request, 'auth/signup.html')
    
def SignOut(request):
    try:
        Auth_token = request.COOKIES.get("Auth_token")
        if Auth_token is not None:
            user = decode(Auth_token)
            if user:
                responce = redirect("/")
                responce.delete_cookie("Auth_token")
                return responce
            else:
                return redirect("/")
        else:
            return redirect("/")
    except Exception as e:  
        return redirect("/login")
def CreateBlog(request):
    if request.method == 'POST':
        Auth_token = request.COOKIES.get("Auth_token")
        user = validateToken(Auth_token)
        if not user:
            return redirect("Login")
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                blog = form.save(commit=False)
                blog.author = user
                blog.slug = slugify(blog.title)
                category_name = request.POST.get('categories')
                if not category_name:
                    messages.error(request, "Please select a category")
                    return render(request, 'blogs/createblog.html', {
                        'form': form,
                        'categories': Categories.objects.all(),
                        'Auth_user': user
                    })
                try:
                    category = Categories.objects.get(id=category_name)
                    blog.categories = category
                except Categories.DoesNotExist:
                    messages.error(request, "Invalid category selected")
                    return render(request, 'blogs/createblog.html', {
                        'form': form,
                        'categories': Categories.objects.all(),
                        'Auth_user': user
                    })
                
                blog.save()
                messages.success(request, "Blog created successfully!")
                return redirect('Home')
                
            except Exception as e:
                print(e)
                messages.error(request, "An error occurred while creating the blog")
                return render(request, 'blogs/createblog.html', {
                    'form': form,
                    'categories': Categories.objects.all(),
                    'Auth_user': user
                })
        else:
            messages.error(request, "Please correct the errors below")
            
    else:
        form = BlogPostForm()
    try:
        Auth_token = request.COOKIES.get("Auth_token")
        user = validateToken(Auth_token)
        print(user)
        if user:
            categories = Categories.objects.all()
            return render(request, 'blogs/createblog.html', {
                'form': form,
                'categories': categories,
                'Auth_user': user
            })
        else:
            return redirect("Login")
    except Exception as e:
        print(e)
        return redirect("Login")
    
def BlogDetails(request,slug):
    try:
        Auth_token = request.COOKIES.get("Auth_token")
        user = validateToken(Auth_token)
        if user:
            user = Blog_User.objects.get(username=user.username)
        else:
            user = None
    except Exception as e:
        user = None
    try:
        blog = Blog.objects.get(slug=slug)
        Auth_token = request.COOKIES.get("Auth_token")
        categories = Categories.objects.all()

        if Auth_token is not None:
            Auth_user = validateToken(Auth_token)
            if Auth_user:
                try:
                    Post_Like.objects.get(blog=blog,user=Auth_user)
                    is_liked = True
                except Exception as e:
                    print(e)
                    is_liked = False
            else:
                is_liked = False
        else:
            is_liked = False
        total_like = Post_Like.objects.filter(blog=blog).count()
        if blog:
            return render(request, 'blogs/blogdetails.html',{"categories":categories,"blog":blog,"blog_count":total_like,"is_liked":is_liked,"Auth_user":user})
        else:
            return redirect("/blogs")
    except Exception as e:
        print(e)
        return redirect("/blogs")
    
def BlogSearch(request):
    query = request.GET.get("q")
    page = int(request.GET.get("page",1))
    if query:
        blogs = Blog.objects.filter(title__icontains=query).order_by('-created_At').values('title','slug','blog_img','author__username','created_At')
        if blogs:
            paginator = Paginator(blogs,10)
            page_obj = paginator.get_page(page)
            result = list(page_obj.object_list)
            print(result)
            return JsonResponse({"results":result},safe=False)
        else:
            return JsonResponse({"results":[]},safe=False)
    else:
        return JsonResponse({"results":[]},safe=False)   

def Follow(request,username):
    if username:
        Auth_token = request.COOKIES.get("Auth_token")
        if Auth_token:
            Auth_user = validateToken(Auth_token)
            if Auth_user:
                user = Blog_User.objects.get(username=username)
                if user:
                    print(user.username)
                    try:
                        follower = Followers.objects.create(follower=Auth_user,following=user)
                        follower.save()
                    except Exception as e:
                        print(e)
                        return JsonResponse({"status":True,"Message":f"You Already Following {user.username}"},safe=False)
                    return JsonResponse({"status":True,"Message":f"You Are Now Following {user.username}"},safe=False)
                else:
                    return JsonResponse({"status":False,"Message":"User Not Found"},safe=False)
            else:
                return JsonResponse({"status":False,"Message":"Please Login"},safe=False)
    else:
        return JsonResponse({"status":False,"Message":"User Not Found"},safe=False)

def Unfollow(request,username):
    if username:
        Auth_token = request.COOKIES.get("Auth_token")
        if Auth_token:
            Auth_user = validateToken(Auth_token)
            if Auth_user:
                user = Blog_User.objects.get(username=username)
                if user:
                    try:
                        follower = Followers.objects.get(follower=Auth_user,following=user)
                        follower.delete()
                        return JsonResponse({"status":True,"Message":f"You Are Now Unfollowing {user.username}"},safe=False)
                    except Exception as e:
                        print(e)
                        return JsonResponse({'status':False,"Message":f"Error Please Try Again Later for : {user.username}"},safe=False)
                else:
                    return JsonResponse({"status":False,"Message":"User Not Found"},safe=False)
            else:
                return JsonResponse({"status":False,"Message":"Please Login"},safe=False)
    else:   
        return JsonResponse({"status":False,"Message":"User Not Found"},safe=False)

def like_Post(request,slug):
    Auth_token = request.COOKIES.get("Auth_token")
    if Auth_token:
        Auth_user = validateToken(Auth_token)
        if Auth_user:
            blog = Blog.objects.get(slug=slug)
            if blog:
                try:
                    like = Post_Like.objects.create(blog=blog,user=Auth_user)
                    like.save()
                    return JsonResponse({"status":True,"Message":f"You Liked This Post"},safe=False)
                except Exception as e:
                    print(e)
                    like = Post_Like.objects.get(blog=blog,user=Auth_user)
                    like.delete()
                    return JsonResponse({"status":True,"Message":"Like Is Removed","removed":True},safe=False)
            else:
                return JsonResponse({"status":False,"Message":"Blog Not Found"},safe=False)
        else:
            return JsonResponse({"status":False,"Message":"Please Login"},safe=False)
    else:
        return JsonResponse({"status":False,"Message":"Please Login"},safe=False)

def Delete_Blog(request,slug):
    Auth_token = request.COOKIES.get("Auth_token")
    if Auth_token:
        Auth_user = validateToken(Auth_token)
        if Auth_user:
            try:
                blog = Blog.objects.get(slug=slug)
                if blog:
                    if blog.author == Auth_user:
                        try:
                            os.remove(f"media/posters/{blog.blog_img}")
                        except Exception as e:
                            print(e)
                        blog.delete()
                        Auth_user.total_blogs -= 1
                        Auth_user.save()
                        return JsonResponse({"status":"200","Message":"Deleted Successfully"},safe=False)
                    else:
                        print("user do not have access to delete this blog")
                        return JsonResponse({"status":"200","Message":"User do not have permisson to Delete the blog"},safe=False)
                else:
                    print("don not found that blog")
                    return JsonResponse({"status":"200","Message":"Blog is missing"},safe=False)
            except Exception as e:
                print(e)
                return JsonResponse({"status":"200","Message":"Blog is missing"},safe=False)
        else:
            print("user is not logged in so it does not have access to delete this")
            return JsonResponse({"status":"200","Message":"user is not logged in"},safe=False)
    else:
        print("same Auth token is not found")
        return JsonResponse({"status":"200","Message":"Token is missing"},safe=False)
def Edit_Blog(request,slug):
    Auth_token = request.COOKIES.get("Auth_token")
    if Auth_token:
        Auth_user = validateToken(Auth_token)
        if Auth_user:
            try:
                categories = Categories.objects.all()
            except Exception as e:
                categories = ""
            try:
                blog = Blog.objects.get(slug=slug)
            except Exception as e:
                print(e)
                return render(request,"404.html",status=404)
            if request.method == "POST":
                form = BlogPostForm(request.POST,request.FILES,instance=blog)
                if form.is_valid():
                    blog = form.save(commit=False)
                    blog.save()
                    return redirect(f"/blogs/{slug}")
                else:
                    return render(request,"blogs/editblog.html",{"form":form,"Auth_user":Auth_user,"categories":categories,"selected_cat":f"{blog.categories.name}"})
            else:
                form = BlogPostForm(instance=blog)
                if form:
                    return render(request,"blogs/editblog.html",{"form":form,"Auth_user":Auth_user,"categories":categories,"selected_cat":f"{blog.categories.name}"})
                else:
                    return render(request,"404.html",status=505)
        else:
            return redirect("/login")
@csrf_exempt
def upload_profile_img(request):
    token = request.COOKIES.get("Auth_token")
    user = token and validateToken(token)
    if not user:
        return redirect("/login")

    if request.method != "POST":
        return JsonResponse({"status":"200","Message":"Invalid Request"}, safe=False)

    upload = request.FILES.get("profile_img")
    if not upload:
        return JsonResponse({"status":"200","Message":"No file uploaded"}, safe=False)

    ext = upload.name.rsplit(".", 1)[-1].lower()
    if ext not in {"jpg","jpeg","png"}:
        return JsonResponse({"status":"200","Message":"Invalid File Format"}, safe=False)

    # delete old
    if user.profile_img:
        user.profile_img.delete(save=False)

    # assign new file and save; this uses GoogleDriveStorage under the hood
    user.profile_img = upload
    user.save()

    return JsonResponse({
        "status":"200",
        "Message":"Image Uploaded Successfully",
        "url": user.profile_img.url
    }, safe=False)
def add_comment(request,slug):
    try:
        Auth_token = request.COOKIES.get("Auth_token")
        user = validateToken(Auth_token)
        if user:
            if slug:
                blog = Blog.objects.get(slug=slug)
                if blog:
                    data = json.loads(request.body)
                    content = data.get('content')
                    parent_id = data.get('parent_id')
                    if not content:
                        return JsonResponse({"status":False,"success":False,"message":"Comment content cannot be empty"},safe=False)
                    if parent_id is not None:
                        parent_comment = Comment.objects.get(id=parent_id)
                        new_comment = Comment.objects.create(
                            post=blog,
                            user=user,
                            content=content,
                            parent=parent_comment
                        )
                        return JsonResponse({"status":True,"success":True},safe=False)
                    else:
                        new_comment = Comment.objects.create(
                            post=blog,
                            user=user,
                            content=content
                        )
                        return JsonResponse({"status":True,"success":True},safe=False)
                else:
                    return JsonResponse({"status":True,"success":False,"message":"Invalid Blog"},safe=False)
            else:
                return JsonResponse({"status":True,"success":False,"message":"Missing Values"},safe=False)
        else:
                return JsonResponse({"status":True,"success":False,"message":"Login To Comment"},safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"status":False,"success":False,"message":"Server Error Please Try Again"},safe=False)