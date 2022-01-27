from .models import Post
from django_filters import FilterSet

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
                 'create': ["lt"],
                 'author': ['exact']
                }
