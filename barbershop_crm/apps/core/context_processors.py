def sidebar_context(request):
    active = ''
    if request.resolver_match:
        active = request.resolver_match.app_name or ''

    user_role = ''
    if request.user.is_authenticated:
        from apps.accounts.mixins import get_user_role
        user_role = get_user_role(request.user)

    return {'active_section': active, 'user_role': user_role}
