from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=150,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Yazar")
    #on_delete ile eğer user silinirse o kullanıcıya ait tüm makalelerde silinme özelliği ekledik.
    title = models.CharField(max_length=50,verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    #Herhangi bir veri eklediğinde o anki tarih direkt olarak created_date özelliğine eklenmiş olacak.
    article_image = models.FileField(blank=True,null=True,verbose_name="Makaleye görsel ekleyin")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Makale",related_name="comments")
    comment_author = models.CharField(max_length=50,verbose_name="İsim")
    comment_content = models.CharField(max_length=200,verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']

class Favorite(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="favorites")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")

    def __str__(self):
        return f"{self.user.username} -> {self.article.title}"
