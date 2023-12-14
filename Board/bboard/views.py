from django.http import HttpResponseRedirect
from django.shortcuts import render
import secrets
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import PostForm, MyUserCreationForm, CommentForm
from .models import DisposableCode, Category
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'



class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author = self.request.user
        post.save()
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'


    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        comment.save()
        return super().form_valid(form)

class CommentDetail(DetailView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            disposable_code = DisposableCode.objects.create(user=user, code = generate_unique_code())
            send_confirmation_email(user, disposable_code.code)
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def generate_unique_code():
    while True:
        code = secrets.token_urlsafe(10)
        if not DisposableCode.objects.filter(code=code).exists():
            break
    return code

def send_confirmation_email(user, confirmation_code):
    subject = 'Account confirmation email'
    message = f'Hello {user.username}, \n\nPlease confirm your registration by clicking the following link:\n\nhttp://127.0.0.1:8000/bboard/confirm/{confirmation_code}'
    send_mail(subject, message, ['noreply@example.com'], [user.email])





def confirmation(request, confirmation_code):
    try:
        disposable_code = DisposableCode.objects.get(code=confirmation_code)
        disposable_code.user.is_active = True
        disposable_code.user.save()
        disposable_code.delete()

        return render(request, 'registration/confirmation_success.html')
    except DisposableCode.DoesNotExist:
        return render(request, 'registration/confirmation_error.html')




@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'you have successfully subscribed to category'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self, *args, **kwargs):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context



