from django.shortcuts import render
from django.views.generic.base import TemplateView
import bleach
from django.urls import reverse
import requests
from nyplapi.views import nyplApiView

class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["error"] = None
        context["data"] = None
        return context
        
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        title = request.POST.get("title", None)
        if not title:
            context["error"] = "Invalid title, please try again!"
            return render(request, self.template_name, context=context)
        title = bleach.clean(title)
        context["data"] = self.get_reading_data(title)
        return render(request, self.template_name, context=context)

    def get_reading_data(self, title):
        api_conenction = nyplApiView()
        res = api_conenction.return_response_data(title)
        return res