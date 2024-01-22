from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .forms import ConatactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser

from .models import News, Category

# Create your views here.

def news_list(request):
    """yangiliklar ro'yxatidan barchasini chiqarish"""
    # news_list = News.objects.all()

    """yangiliklar ro'yxatidan statusi faqat published bo'lganlarinigina chiqarish"""
    # 1-usul
    # news_list = News.objects.filter(status=News.Status.Published)
    # 2-usul
    news_list = News.published.all()  # o'zimiz yaratgan managerdan foydalanib

    context = { 'news_list': news_list }
    return render(request, "news/news_list.html", context=context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)
    context = {}
    # hitcount logik
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi comment obyektini yaratamiz lekin MB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            # izohni izh yozilayotgan yangilik bilan bog'laymiz
            new_comment.news = news
            # izoh egasini so'rov yuborayotgan user bilan bog'laymiz
            new_comment.user = request.user
            # yangi izohni MB ga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, "news/news_detail.html", context)

# CLASSLAR BILAN BERILGANDA:
# class NewsList(ListView):
#     model = News
#     template_name = 'news_list.html'
#     context_object_name = 'news_list'
#
class NewsDetail(DetailView):
    # specify the model to use
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    # override context data
    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ma'lum yangilik obyekti
        news = News.objects.filter(slug = slug)
        comments = news.comments.filter(active=True)
        new_comment = None
        comment_form = CommentForm()

        if self.request.method == 'POST':
            comment_form = CommentForm(data=self.request.POST)
            if comment_form.is_valid():
                # Yangi izoh obyektini yaratish
                new_comment = comment_form.save(commit=False)
                new_comment.news = news
                new_comment.user = self.request.user
                new_comment.save()
                # Izoh yuborilgach, formani yangilab qo'yish
                comment_form = CommentForm()
        context['news'] = news
        context['comments'] = comments
        context['new_comment'] = new_comment
        context['comment_form'] = comment_form
        return context

# def index_view(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by("-publish_time")[:5]
#     local_one = News.published.filter(category__name='Mahalliy').order_by("-publish_time")[:1]
#     local_news = News.published.all().filter(category__name='Mahalliy')[1:4]
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_one': local_one,
#         'local_news': local_news
#     }
#     return render(request, 'news/index.html', context)


class IndexView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by("-publish_time")[:5]
        context['local_one'] = News.published.filter(category__name='Mahalliy').order_by("-publish_time")[:1]
        context['local_news'] = News.published.all().filter(category__name='Mahalliy')[1:5]
        context['techno_one'] = News.published.filter(category__name='Texnologiya').order_by("-publish_time")[:1]
        context['techno_news'] = News.published.all().filter(category__name='Texnologiya')[1:5]
        context['foreign_one'] = News.published.filter(category__name='Xorij').order_by("-publish_time")[:1]
        context['foreign_news'] = News.published.all().filter(category__name='Xorij')[1:5]
        context['sport_one'] = News.published.filter(category__name='Sport').order_by("-publish_time")[:1]
        context['sport_news'] = News.published.all().filter(category__name='Sport')[1:5]
        return context



class LocalView(ListView):
    model = News
    template_name = 'news/local.html'
    context_object_name = 'mahalliy'

    def get_queryset(self):
        news = self.model.published.all().order_by('-publish_time').filter(category__name = 'Mahalliy')[:20]
        return news



class ForeignView(ListView):
    model = News
    template_name = 'news/foreign.html'
    context_object_name = 'xorij'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Xorij')
        return news



class TechnologyView(ListView):
    model = News
    template_name = 'news/technology.html'
    context_object_name = 'texnologiya'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Texnologiya')
        return news



class SportView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Sport')
        return news


# def contact_view(request):
#     form = ConatactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")
#
#     context = {
#         'form': form
#     }
#     return render(request, 'news/contact.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ConatactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kvargs):
        form = ConatactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")

        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)



class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title_uz', 'title_ru', 'title_en', 'slug', 'body_uz', 'body_ru', 'body_en', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'



class NewsDeleteViews(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('index_page')



class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    fields = ('title_uz', 'title_ru', 'title_en', 'slug', 'body_uz', 'body_ru', 'body_en', 'image', 'category', 'status')
    template_name = 'crud/news_create.html'

    def save(self, *args, **kwargs):
        self.model.slug = slugify(self.model.title)
        self.save(*args, **kwargs)


def about_view(request):
    context = {

    }
    return render(request, 'news/single_page.html')


def _404_page(request):
    context = {

    }
    return render(request, 'news/404.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    print(admin_users)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView): # testdriven.io saytida qidiruv tizimini mukammal qilish yo'llari berilgan
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            # icontains (contains dan farqli tomoni) katta-kichik harflarni farqlamaydi
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    