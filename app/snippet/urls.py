from django.urls import path
from app.snippet.views import SnippetAddView, SnippetListView, SnippetDetailView, \
    SnippetUpdateView, SnippetDeleteView, TagListView, TagDetailView

urlpatterns = [
    path('snippet/add/',SnippetAddView.as_view(), name="add"),
    path('snippet/list/', SnippetListView.as_view(), name='list'),
    path('snippet/details/<id>/', SnippetDetailView.as_view(), name='details'),
    path('snippet/update/<id>/', SnippetUpdateView.as_view(), name='update'),
    path('snippet/delete/<id>/', SnippetDeleteView.as_view(), name='update'),
    path('tag/list/', TagListView.as_view(), name='tag_list'),
    path('tag/details/<id>/', TagDetailView.as_view(), name='details'),
]