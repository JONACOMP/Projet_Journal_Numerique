from django.views.generic import View
from django.shortcuts import render, redirect

from Accounts.forms import SignUpForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST,request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect("accounts:signin")
        context = {"form": forms}
        return render(request, self.template_name, context)
