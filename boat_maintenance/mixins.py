from django.contrib.auth.mixins import AccessMixin


class UserNotShareOwner(AccessMixin):
    """Verify that the current user is authenticated and not a Share Owner."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile == "SO":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
