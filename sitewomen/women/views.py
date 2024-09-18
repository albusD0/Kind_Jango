from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, \
    HttpResponsePermanentRedirect, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View

from .forms import AddPostForm
from .models import Women, PublishedModel, Category, TagPost, UploadFiles

from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView, UpdateView
from .forms import *
from .utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# class AddPost(CreateView):
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    title_page = 'Главная страница'
    cat_selected = 0
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'cat_selected': 0}
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

def about(request):
    contact_list = Women.objects.filter(is_published=True)
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'page_obj': page_obj})



class ShowPost(DataMixin, DetailView):
    #model = Women
    template_name = 'women/post.html'
    context_object_name = 'women'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['women'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

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

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         return render(request, 'women/addpage.html', {'menu': menu, 'title': "Добавление статьи", 'form': form})
#
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # сохранение данных формы в БД для Model
#             return redirect('home')
#         return render(request, 'women/addpage.html', {'menu': menu, 'title': "Добавление статьи", 'form': form})

class AddPage(CreateView):
    # form_class = AddPostForm
    model = Women
    fields = ['title', 'slug', 'content', 'is_published', 'cat', 'photo']
    template_name = 'women/addpage.html'
    #success_url = reverse_lazy('home')

    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

    # def form_valid(self, form): # Если используем CreateView то эта функция не нужна (FormView)
    #     form.save()
    #     return super().form_valid(form)

class UpdatePage(UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat', ]
    template_name = 'women/addpage.html'

    extra_context = {
        'menu': menu,
        'title': 'Редактирование статьи',
    }
def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['women_list'][0].cat)
        context['cat_selected'] = context['women_list'][0].cat_id
        return context

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

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None, }
#     return render(request, 'women/index.html', context=data)


# class ShowPostsByTag(DataMixin, ListView):
#     model = Women
#     template_name = 'women/index.html'
#
#     def get_queryset(self):
#         return Women.objects.filter(tags__slug=self.kwargs['tag_slug'])

class ShowPostsByTag(DataMixin, View):
    def get(self, request, **kwargs):
        tag = get_object_or_404(TagPost, slug=kwargs['tag_slug'])
        posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)
        data = {
            'title': f'Тег: {tag.tag}',
            'women_list': posts, }
        return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
