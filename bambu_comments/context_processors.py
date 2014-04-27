from bambu_comments.models import Comment

def latest(request):
    return {
        'latest_comments': Comment.objects.live
    }