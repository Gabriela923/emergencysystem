from emergency import models


def per_mess(request):
    ms = request.session.get('username')
    per_obj = models.UserInfo.objects.filter(username=ms).first()
    per_id = per_obj.id
    return per_id