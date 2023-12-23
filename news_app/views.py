from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .forms import ConatactForm

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

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, "news/news_detail.html", context)

# CLASSLAR BILAN BERILGANDA:
# class NewsList(ListView):
#     model = News
#     template_name = 'news_list.html'
#     context_object_name = 'news_list'
#
# class NewsDetail(DetailView):
#     model = News
#     template_name = 'news_detail.html'

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
        news = self.model.published.all().filter(category__name = 'Mahalliy')
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



def about_view(request):
    context = {

    }
    return render(request, 'news/single_page.html')


def _404_page(request):
    context = {

    }
    return render(request, 'news/404.html', context)
