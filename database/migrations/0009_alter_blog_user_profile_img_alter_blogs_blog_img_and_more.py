# Generated by Django 5.1.5 on 2025-04-23 13:45

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_alter_blog_user_profile_img_alter_blogs_blog_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_user',
            name='profile_img',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_img',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='blogs'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='categories'),
        ),
    ]
