from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restringe una vista a ciertos roles. Ej: allowed_roles = ("SUPERADMIN",)."""

    allowed_roles: tuple = ("ADMIN", "SUPERADMIN")

    def test_func(self):
        return self.request.user.role in self.allowed_roles
