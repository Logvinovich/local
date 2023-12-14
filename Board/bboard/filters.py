from django_filters import FilterSet, ModelChoiceFilter
from .models import Comment, Post

class PostFilter(FilterSet):
    post = ModelChoiceFilter(
        empty_label='all posts',
        field_name='post',
        label='filter',
        queryset=Comment.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('post',)

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])