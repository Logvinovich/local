from django.urls import path
from .views import IndexView

app_name='protect'

urlpatterns = [
    path('', IndexView.as_view()),
    path('delete/<int:comment_id>', IndexView.delete_comment, name='delete'),
    path('accept/<int:comment_id>', IndexView.accept_comment, name='accept')
]