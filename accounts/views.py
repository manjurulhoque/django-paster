from django.contrib import messages, auth
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, ListView
from .forms import *
from pasteapp.models import *


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/form.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)
        # return super(Login, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        # checking for email if is already taken or not
        # username is by default unique
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, 'This email is already taken')
            return redirect('accounts:register')

        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/form.html', {'form': user_form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/form.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    # @method_decorator(sensitive_post_parameters('password'))
    # @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         redirect_to = self.get_success_url()
    #         return HttpResponseRedirect(redirect_to)
    #     # return super().dispatch(self.request, *args, **kwargs)
    #     return super(Login, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())
        # return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('pasteapp:home')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class MyPastesListView(ListView):
    model = Paste
    template_name = 'accounts/my-pastes.html'
    context_object_name = 'pastes'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(request, "Please sign in to view this page")
            return HttpResponseRedirect(reverse_lazy('pasteapp:home'))
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.pastes.all()
