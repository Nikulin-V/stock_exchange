from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Home page"""
    template = 'homepage/home.html'

    def get(self, request):
        return render(request, self.template)
