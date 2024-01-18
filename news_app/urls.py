from django.urls import path
from .views import IndexView, ContactPageView, about_view, _404_page, news_list, news_detail, NewsDetail, \
    LocalView, ForeignView, TechnologyView, SportView, NewsUpdateView, NewsDeleteViews, NewsCreateView, \
    admin_page_view, SearchResultsList

urlpatterns = [
    path('', IndexView.as_view(), name = 'index_page'),
    path('news/', news_list, name='all_news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:slug>/', news_detail, name='news_detail_page'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<slug>/delete/', NewsDeleteViews.as_view(), name='news_delete'),

    path('contact-us/', ContactPageView.as_view(), name = 'contact_page'),
    path('about-us/', about_view, name='about_page'),
    path('local/', LocalView.as_view(), name = 'local_news_page'),
    path('foreign/', ForeignView.as_view(), name = 'foreign_news_page'),
    path('technology/', TechnologyView.as_view(), name = 'techno_news_page'),
    path('sport/', SportView.as_view(), name = 'sport_news_page'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_result')
]
