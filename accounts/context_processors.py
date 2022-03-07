from django.shortcuts import get_object_or_404

from accounts.models import Profile


def profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    return {"user_profile": user_profile}
