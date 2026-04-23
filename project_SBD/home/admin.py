from django.contrib import admin
from .models import HomePageContent, Product, ProductCategory, Project, ProjectCategory, Post, PostCategory, QnA

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(Product)
admin.site.register(ProductCategory)
#########################
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(HomePageContent)
admin.site.register(QnA)
