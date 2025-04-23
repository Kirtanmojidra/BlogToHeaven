from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField
from cloudinary.models import CloudinaryField

class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    image = CloudinaryField('categories',null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_categories'  

class Blog_User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    profile_img = CloudinaryField('profile',null=True)
    bio = models.TextField(max_length=500, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'blog_users'

class Blogs(models.Model):
    STATUS = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]
    title = models.CharField(max_length=200)
    content = QuillField(max_length=6000)
    author = models.ForeignKey(Blog_User, on_delete=models.CASCADE, related_name='blogs')
    blog_img = CloudinaryField('blogs',null=True)
    slug = models.SlugField(unique=True, blank=True)
    status = models.CharField(max_length=10,choices=STATUS, default='Published')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='blogs')
    likes = models.ManyToManyField(Blog_User, through='Post_Like', related_name='liked_blogs')
    created_At = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_At = models.DateTimeField(auto_now=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    class Meta:
        db_table = 'blog_posts'

class Post_Like(models.Model):
    user = models.ForeignKey(Blog_User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        unique_together = ('user', 'blog')
        db_table = 'blog_post_likes'

    def __str__(self):
        return f"{self.user.username} liked {self.blog.title}"

class Followers(models.Model):
    follower = models.ForeignKey(Blog_User, on_delete=models.CASCADE, related_name='following_users')
    following = models.ForeignKey(Blog_User, on_delete=models.CASCADE, related_name='followers_users')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        unique_together = ('follower', 'following')
        db_table = 'blog_followers'

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Comment(models.Model):
    post = models.ForeignKey(Blogs, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Blog_User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def isReply(self):
        return self.parent is not None

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"

    class Meta:
        db_table = 'blog_comments'