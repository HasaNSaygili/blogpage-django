from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse

from article.models import Article,Comment,Category
from .forms import ArticleForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    context = {
        "number1":20
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")

#Dinamik url yapısı kurduk.
"""
def detail(request,id):
    return HttpResponse("dETAİL"+str(id))
"""

@login_required(login_url= "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    favorites = request.user.favorites.select_related("article", "article__author", "article__category").all()
    context = {
        "articles":articles,
        "favorites": favorites,
    }
    return render(request,"dashboard.html",context)

@login_required(login_url= "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale başarıyla eklendi...")
        return redirect("article:dashboard")
    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article,id = id) # istenen id'ye ait bir makale yoksa 404 not found hatası dönecek.

    comments = article.comments.filter(parent__isnull=True)
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id)[:6]
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = article.favorited_by.filter(user=request.user).exists()

    return render(request,"detail.html",{"article":article,"comments":comments,"related_articles":related_articles,"is_favorited":is_favorited})



@login_required(login_url= "user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    if article.author != request.user:
        messages.error(request, "Bu makaleyi düzenleme yetkiniz yok.")
        return redirect("article:dashboard")
    form = ArticleForm(request.POST or None , request.FILES or None,instance = article)
    #instance ile makalenin o anki halini aldık.

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale başarıyla güncellendi...")
        return redirect("article:dashboard")
    
    return render(request,"update.html",{"form":form})

@login_required(login_url= "user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    if article.author != request.user:
        messages.error(request, "Bu makaleyi silme yetkiniz yok.")
        return redirect("article:dashboard")
    article.delete()
    
    messages.success(request,"Makale başarıyla silindi...")
    return redirect("article:dashboard")


def articles(request):

    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        categories = Category.objects.all()
        return render(request,"articles.html",{"articles":articles,"categories":categories})
    articles = Article.objects.all()
    categories = Category.objects.all()
    #Tüm articleları aldık
    return render(request,"articles.html",{"articles":articles,"categories":categories})

def addComment(request,id):
    article = get_object_or_404(Article,id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        parent_id = request.POST.get("parent_id")

        newComment = Comment(comment_author=comment_author,comment_content=comment_content)

        newComment.article = article
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id, article=article)
                newComment.parent = parent
            except Comment.DoesNotExist:
                pass

        newComment.save()
        
    return redirect(reverse("article:detail",kwargs = {"id":id}))


def category_articles(request,slug):
    category = get_object_or_404(Category,slug=slug)
    articles = Article.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request,"category_articles.html",{"category":category,"articles":articles,"categories":categories})

@login_required(login_url= "user:login")
def toggle_favorite(request, id):
    article = get_object_or_404(Article, id=id)
    fav, created = article.favorited_by.get_or_create(user=request.user)
    if not created:
        fav.delete()
        messages.info(request, "Favorilerden çıkarıldı.")
    else:
        messages.success(request, "Favorilere eklendi.")
    return redirect(reverse("article:detail", kwargs={"id": id}))