from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

from .models import Category, Husband, Women


# class AddPostForm(forms.Form): Этот вариант для форм не связанных с Models
#     title = forms.CharField(error_messages={'required': 'Без заголовка никак'}, min_length=5, max_length=255, label='Заголовок',  widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label='URL', validators=[MinLengthValidator(5, message='Минимум 5 символов'), MaxLengthValidator(100, message='Максимум 100 символов')])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
#     is_published = forms.BooleanField(required=False, label='Статус', initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
#     #husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Супруг', empty_label='Не замужем')
#     photo = forms.ImageField(label='Фото', required=False)
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")

class AddPostForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, label='Статус', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': "URL"}

    def clean_title(self): # пользовательский валидатор (без класса)
         title = self.cleaned_data['title']
         if len(title) >50:
             raise ValidationError('Длина превышает 50 символов')