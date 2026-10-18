from django.urls import path
from .views import TerminalExecuteView

app_name = 'terminal'

urlpatterns = [
    path('execute/', TerminalExecuteView.as_view(), name='terminal-execute'),
]

