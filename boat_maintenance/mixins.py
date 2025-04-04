from django.contrib.auth.mixins import LoginRequiredMixin

class UserNotShareOwner(LoginRequiredMixin):
    """Verify that the current user is not a Share Owner."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile == "SO":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
