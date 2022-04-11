from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from accounts.models import Profile


def profile(request):
    user_profile = []
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
    return {"user_profile": user_profile}
