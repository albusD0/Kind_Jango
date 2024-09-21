from django.urls import path, re_path, register_converter
from . import views
from . import converters
from .views import WomenHome, WomenCategory, ShowPost, UpdatePage, ShowPostsByTag, SearchResultsView

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('about/', views.about, name='about'),
    #path('addpage/', views.addpage, name='add_page'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    # path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/',  WomenCategory.as_view(), name='category'),
    #path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('tag/<slug:tag_slug>/', ShowPostsByTag.as_view(), name='tag'),
    path('edit/<int:pk>/', UpdatePage.as_view(), name='edit_page'),

]
