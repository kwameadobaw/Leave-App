def user_profile(request):
    """
    Context processor to add user profile information to all templates
    """
    context = {}
    if request.user.is_authenticated:
        try:
            context['user_profile'] = request.user.userprofile
            context['user_type'] = request.user.userprofile.user_type
        except AttributeError:
            # Handle case where user doesn't have a profile
            context['user_profile'] = None
            context['user_type'] = None
    return context