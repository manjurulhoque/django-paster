import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import FormView, CreateView, DetailView, RedirectView
from .models import *
from .forms import *


class HomeView(CreateView):
    template_name = 'home.html'
    form_class = CreatePasteForm
    extra_context = {
        'title': 'Home',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_syntaxes'] = Syntax.objects.filter(popular=True, active=True)
        context['all_syntaxes'] = Syntax.objects.filter(popular=False, active=True)
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(HomeView, self).form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # form.fields['slug'].initial = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return form

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('pasteapp:paste-details', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # request post is immutable
        # when need to make mutable first
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['slug'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        request.POST._mutable = mutable
        # form.data['slug'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.object = None
        if form.is_valid():
            messages.success(request, "Paste successfully created")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PasteDetailsView(DetailView):
    model = Paste
    slug_field = 'slug'
    template_name = 'show.html'
    context_object_name = 'paste'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        viewed = request.session.get('viewed', [])
        if viewed:
            if self.object.id not in viewed:
                viewed.append(self.object.id)
                request.session['viewed'] = viewed
                self.object.views += 1
                self.object.save()
        else:
            viewed = [self.object.id]
            request.session['viewed'] = viewed
            self.object.views += 1
            self.object.save()
        if self.object.expire_time:
            if self.object.expire_time < timezone.now():
                messages.warning(request, "Paste is expired")
                return HttpResponseRedirect(reverse_lazy('pasteapp:home'))
        return self.render_to_response(context)


class DownloadView(View):
    def get(self, request, *args, **kwargs):
        paste = Paste.objects.get(slug=kwargs['slug'])
        extension = 'txt' if paste.language_syntax() is None else paste.language_syntax().extension
        response = HttpResponse(content=paste.content)
        response['Content-Disposition'] = 'attachment; filename={}.{}'.format(paste.title, extension)
        return response


class CloneCreateView(CreateView):
    model = Paste
    template_name = 'clone.html'
    form_class = CreatePasteForm
    slug_field = 'slug'
    slug = None

    def get(self, request, *args, **kwargs):
        self.object = None
        self.slug = kwargs['slug']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # request post is immutable
        # when need to make mutable first
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['slug'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        request.POST._mutable = mutable
        # form.data['slug'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.object = None
        if form.is_valid():
            messages.success(request, "Paste successfully created")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paste'] = get_object_or_404(self.model, slug=self.slug)
        context['popular_syntaxes'] = Syntax.objects.filter(popular=True, active=True)
        context['all_syntaxes'] = Syntax.objects.filter(popular=False, active=True)
        return context

    def get_success_url(self):
        return reverse_lazy('pasteapp:paste-details', kwargs={'slug': self.object.slug})


class CloneRedirectView(RedirectView):
    permanent = False
    pattern_name = 'pasteapp:paste-clone'
