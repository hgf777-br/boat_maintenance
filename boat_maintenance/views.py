from django.urls import reverse
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('user:table-users'))