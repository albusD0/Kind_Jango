from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View

from .forms import AddPostForm
from .models import Women, PublishedModel, Category, TagPost, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .forms import *

# class AddPost(CreateView):
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0}
    #context_object_name = 'posts'
    def get_queryset(self):
        return Women.objects.filter(is_published=True)

# def index(request):
#     posts = Women.published.all()
#     data = {
#         #'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)

# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def about(request, form=None):
    #files = form.cleaned_data["files"] #UploadedFile.objects.all()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        for uploaded_file in request.FILES.getlist('files'):
            #handle_uploaded_file(uploaded_file)#UploadedFile.objects.create(file=uploaded_file)
            fp = UploadFiles(file=uploaded_file)
            fp.save()
        return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})



class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'women/post.html', context=data)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data) - это вывод в консоли
#     #         try: а этот вариант для формы не связанной с Model
#     #             Women.objects.create(**form.cleaned_data)
#     #             return redirect('home')
#     #         except:
#     #             form.add_error(None, 'Ошибка добавления поста')
#             form.save() # сохранение данных формы в БД для Model
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'menu': menu, 'title': "Добавление статьи", 'form': form})

class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        return render(request, 'women/addpage.html', {'menu': menu, 'title': "Добавление статьи", 'form': form})


    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # сохранение данных формы в БД для Model
            return redirect('home')
        return render(request, 'women/addpage.html', {'menu': menu, 'title': "Добавление статьи", 'form': form})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")

class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    allow_empty = False
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0}
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk)
#     data = {
#         'title': f"Рубрика: {category.name}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None, }
    return render(request, 'women/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
