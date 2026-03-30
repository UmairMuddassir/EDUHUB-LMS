"""Reusable access-control mixins."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only allow authenticated Instructors."""

    def test_func(self):
        return self.request.user.is_instructor

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Only instructors can access this page.")
        return super().handle_no_permission()


class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only allow authenticated Students."""

    def test_func(self):
        return self.request.user.is_student

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Only students can access this page.")
        return super().handle_no_permission()
