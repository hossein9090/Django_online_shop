import itertools
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.models import User
from django.shortcuts import render

from order.forms import UserNewOrderForm
from products.models import Product
from products_category.models import ProductCategory
from sliders.models import Slider
from shop_settings.models import SiteSetting
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


def header(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    console = ProductCategory.objects.filter(pack="console").all()
    accessories = ProductCategory.objects.filter(pack="accessories").all()
    disk = ProductCategory.objects.filter(pack="disk").all()
    pc = ProductCategory.objects.filter(pack="pc").all()
    other = ProductCategory.objects.filter(pack="other").all()
    context = {
        'console': console,
        'accessories': accessories,
        'disk': disk,
        'pc': pc,
        'other': other,
        'setting': site_setting,
    }
    return render(request, 'shared/Header.html', context)


# footer code behind
def footer(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request, 'shared/Footer.html', context)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


# code behind
def home_page(request):
    sliders = Slider.objects.all()
    # most_visit_products = Product.objects.order_by('-visit_count').all()[:8]
    most_visit_products1 = Product.objects.order_by('-visit_count').all()
    # latest_products = Product.objects.order_by('-id').all()[:8]
    latest_products1 = Product.objects.order_by('-id').all()
    # ps4game = ProductCategory.objects.filter(id=7).all()
    allcat = ProductCategory.objects.all()

    # selected_product_id = kwargs['productId']
    # new_order_form = UserNewOrderForm(request.POST or None, initial={'product_id': selected_product_id})

    context = {
        'data': 'این سایت فروشگاهی با فریم ورک django نوشته شده',
        'sliders': sliders,
        # 'most_visit': my_grouper(4, most_visit_products),
        'most_visit1': most_visit_products1,
        # 'latest_products': my_grouper(4, latest_products),
        'latest_products1': latest_products1,
        'allcat': allcat,

        # 'new_order_form': new_order_form,

    }
    return render(request, 'home_page.html', context)


def about_page(request):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting
    }

    return render(request, 'about_page.html', context)


def handle_404_error(request, exception):
    return render(request, '404.html', {})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_email_file.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="account/password.html",
                  context={"password_reset_form": password_reset_form})
