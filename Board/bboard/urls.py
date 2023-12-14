from django.urls import path
from .views import PostList, PostDetail, PostCreate,CommentCreate, CommentDetail, CategoryListView, PostUpdate, confirmation, register, subscribe
from django.contrib.auth.views import LoginView, LogoutView


app_name='bboard'
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_add'),
    path('comment/', CommentCreate.as_view(), name='comment_add'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment_detail'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_edit'),
    path('register/', register, name='register'),
    path('confirm/<str:confirmation_code>/', confirmation, name='confirm'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')

]