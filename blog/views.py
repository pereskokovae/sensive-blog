from django.shortcuts import render
from blog.models import Comment, Post, Tag
from django.db.models import Count


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_amount,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.first().title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts,
    }


def index(request):
    popular_posts = Post.objects.popular().prefetch_related('author')[:5]
    Post.objects.fetch_with_comments_count(popular_posts)

    fresh_posts = Post.objects.annotate(
        comments_amount=Count("comments")
        ).order_by('published_at').prefetch_related('author')
    most_fresh_posts = list(fresh_posts)[-5:]

    most_popular_tags = Tag.objects.popular().annotate(Count('posts'))[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in popular_posts
            ],
        'page_posts': [
            serialize_post(post) for post in most_fresh_posts
            ],
        'popular_tags': [
            serialize_tag(tag) for tag in most_popular_tags
            ],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.annotate(
        likes_amount=Count('likes'),
        distinct=True
        ).prefetch_related('author').get(slug=slug)
    comments = Comment.objects.filter(post=post).select_related('author')
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_amount,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    popular_posts = Post.objects.popular().prefetch_related('author')[:5]

    for post in popular_posts:
        post.comments_amount = Post.objects.fetch_with_comments_count()[post.id]

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.annotate(Count('posts')).get(title=tag_title)

    most_popular_tags = Tag.objects.popular()[:5]

    popular_posts = Post.objects.popular().prefetch_related('author')[:5]

    for post in popular_posts:
        post.comments_amount = Post.objects.fetch_with_comments_count()[post.id]

    related_posts = tag.posts.annotate(comments_amount=Count(
        'comments',
        distinct=True
        ))[:20]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
