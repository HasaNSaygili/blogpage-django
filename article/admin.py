from django.contrib import admin

from .models import Article,Comment,Category
#Kendi ARTICLE modelimizi import ettik.

# Register your models here.
#admin.site.register(Article)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title","author","category","created_date"]

    list_display_links = ["title","created_date"]

    search_fields = ["title"]

    list_filter = ["created_date","category"]
    
    class Meta:
        model = Article
#ArticleAdmin ve Article modelini eşlemek için Meta sınıfınıyazdık.


admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_display_links = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    
    class Meta:
        model = Category