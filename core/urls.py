from django.urls import path

from . import views

urlpatterns = [
  path("lebert/",views.lebertCreateView.as_view()),
  path("lcf/",views.lcfCreateView.as_view()),
  path("history/",views.historyListView.as_view())
]