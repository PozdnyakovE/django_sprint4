from datetime import date

from .models import Post


def get_post_list():
    """Возвращает список постов, отсортированных по дате."""
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=date.today()
    ).order_by('-pub_date')
    return post_list
