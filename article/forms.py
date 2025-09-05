from django import forms
from .models import Article
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","article_image","category"]
#Model form kullanarak Article modelimizden form oluşturduk. Ama sadece title ve content alanları için input alanı istedik.