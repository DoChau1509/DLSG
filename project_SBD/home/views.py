# views.py
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.utils.http import url_has_allowed_host_and_scheme
from functools import wraps
from urllib.parse import urlparse
from .forms import UserRegistrationForm, LoginForm
from .forms import HomePageContentForm

from .models import (
    HomePageContent,
    Product,
    ProductCategory,
    Project,
    ProjectCategory,
    Post,
    PostCategory,
    QnA,
)


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")

        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        messages.warning(request, "Bạn không có quyền truy cập trang quản lý.")
        return redirect("home")

    return _wrapped


def _is_management_path(path: str) -> bool:
    if not path:
        return False

    management_prefixes = (
        "/dashboard",
        "/project/add",
        "/project/edit",
        "/project/delete",
        "/products",
        "/product/add",
        "/product/edit",
        "/product/delete",
        "/project-category",
        "/product-category",
        "/posts",
        "/post/add",
        "/post/edit",
        "/post/delete",
        "/post-category",
        "/home-content/edit",
    )
    return path.startswith(management_prefixes)


def _get_home_page_content():
    return HomePageContent.objects.get_or_create(
        pk=1,
        defaults={
            "intro_title": "Giới thiệu lộ trình",
            "intro_description": (
                "Lộ trình này được thiết kế đặc biệt dành cho du khách trong nước và quốc tế "
                "cũng như người dân địa phương mong muốn trải nghiệm nhịp sống trung tâm "
                "Thành phố Hồ Chí Minh một cách chậm rãi, sâu sắc và thân thiện với môi trường."
            ),
        },
    )[0]


# ====================== PUBLIC PAGES ======================
def home(request):
    posts = Post.objects.order_by("created_at", "-id")
    home_content = _get_home_page_content()
    return render(
        request,
        "home/home.html",
        {"posts": posts, "home_content": home_content},
    )


def contact(request):
    qnas = QnA.objects.filter(is_published=True).order_by("-created_at", "-id")
    return render(request, 'home/contact.html', {"qnas": qnas})


# ====================== CRUD PROJECT ======================
    category, _ = ProductCategory.objects.get_or_create(
        name="Chưa phân loại",
        defaults={"slug": "uncategorized", "is_hidden": True},
    )
    return category

@staff_required
def qna_create(request):
    if request.method == 'POST':
        QnA.objects.create(
            question = request.POST.get('question'),
            answer = request.POST.get('answer'),
        )
        return redirect('post_list')
    return render(request, 'home/qna_form.html')\
        
@staff_required
def qna_update(request, id):
    qna = get_object_or_404(QnA, id=id)
    if request.method == 'POST':
        qna.question = request.POST.get('question')
        qna.answer = request.POST.get('answer')
        qna.save()
        return redirect('post_list')
    return render(request, 'home/qna_form.html', {'qna': qna})

@staff_required
def qna_delete(request, id):
    qna = get_object_or_404(QnA, id=id)
    qna.delete()
    return redirect('post_list')
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('dashboard')


# ====================== AUTH ======================
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect("dashboard")
        return redirect("home")

    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_path = None
            if next_url:
                next_path = urlparse(next_url).path

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ) and ((user.is_staff or user.is_superuser) or not _is_management_path(next_path)):
                return redirect(next_url)

            if user.is_staff or user.is_superuser:
                return redirect("home")
            return redirect("home")
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {
        'form': form,
        'next': next_url,
    })

def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect("dashboard")
        return redirect("home")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Đăng ký thành công.")

            next_path = None
            if next_url:
                next_path = urlparse(next_url).path

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ) and not _is_management_path(next_path):
                return redirect(next_url)
            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form, "next": next_url})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        logout(request)
        return redirect("home")

    return render(request, "accounts/logout.html")

    projects = Project.objects.all().order_by('-id')
    products = Product.objects.all().order_by("-id")
    return render(request, 'home/dashboard.html', {'projects': projects, "products": products})


@staff_required
def home_content_update(request):
    home_content = _get_home_page_content()

    if request.method == "POST":
        form = HomePageContentForm(request.POST, instance=home_content)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã cập nhật phần giới thiệu lộ trình.")
            return redirect("home_content_edit")
    else:
        form = HomePageContentForm(instance=home_content)

    return render(
        request,
        "home/home_content_form.html",
        {"form": form},
    )


# ====================== CRUD POST ======================
@staff_required
def post_list(request):
    posts = Post.objects.all().order_by("-id")
    return render(request, "home/post_list.html", {"posts": posts})

def qna_list(request):
    qnas = QnA.objects.all().order_by("-id")
    return render(request, "home/qna_list.html", {"qnas": qnas})


def post_public(request):
    posts = Post.objects.all().order_by("-created_at", "-id")
    return render(
        request,
        "home/post.html",
        {"posts": posts},
    )


def post_detail(request, id):
    post = get_object_or_404(Post.objects, id=id)
    return render(request, "home/post_detail.html", {"post": post})


@staff_required
def post_create(request):
    if request.method == "POST":
        Post.objects.create(
            title=request.POST.get("title"),
            summary=request.POST.get("summary", ""),
            content=request.POST.get("content"),
            image=request.FILES.get("image"),
        )
        return redirect("post_list")

    return render(request, "home/post_form.html")


@staff_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.summary = request.POST.get("summary", "")
        post.content = request.POST.get("content")

        if "image" in request.FILES:
            post.image = request.FILES["image"]

        post.save()
        return redirect("post_list")

    return render(
        request,
        "home/post_form.html",
        {"post": post},
    )


@staff_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("post_list")
