import pyshorteners
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import UrlForm
from .models import Urls


def index(request):
    return render(request, 'main_page.html')

def url_creator(url):
    s = pyshorteners.Shortener()
    cut = s.tinyurl.short(url)
    return cut

from django.shortcuts import render
def convent(request):
    submitbutton = request.POST.get("submit")
    original_url = ''
    cut_ul = ''
    form = UrlForm(request.POST or None)
    if form.is_valid():
        original_url = form.cleaned_data.get("original_url")
        cut_ul = url_creator(original_url)
        form.cut_url = cut_ul
        # form.save()
        save_conv(request, original_url, cut_ul)
    print(request.user.pk)
    context = {'form': form, 'original_url': original_url, 'cut_url': cut_ul, 'submitbutton': submitbutton}
    return render(request, 'conventer.html', context)


def save_conv(request, ou, cu):
    ur = Urls.objects.all()
    c = Urls.objects.count()
    k = 0
    for i in ur:
        if str(i.original_url)==str(ou):
            k += 1
    if k == 0:
        u = Urls()
        u.original_url = ou
        u.cut_url = cu
        u.using_id=request.user.pk
        u.save()
    else:
        print('Уже сократили ссылку')


class UrlsByUser(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Urls
    template_name ='usersurls.html'
    paginate_by = 10

    def get_queryset(self):
        c = Urls.objects.filter(using=self.request.user).count()
        return Urls.objects.filter(using=self.request.user)

from .forms import UserRegistrationForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

