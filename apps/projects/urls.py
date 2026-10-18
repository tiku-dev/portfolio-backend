from django.urls import path
from .views import ProjectListView, ProjectDetailView, TagListView, ProjectLivePingView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<slug:slug>/ping/', ProjectLivePingView.as_view(), name='project-ping'),
]

