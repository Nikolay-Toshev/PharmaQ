from PharmaQ.rating.models import Rating


def get_pharmacist_rating(user):
    likes = Rating.objects.filter(answer_id__creator_id=user, like__exact=True).count()
    dislikes = Rating.objects.filter(answer_id__creator_id=user, dislike__exact=True).count()
    rating = likes - dislikes
    return rating

