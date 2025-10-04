from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Tag
from .forms import CustomUserCreationForm, ProfileForm, PostForm, CommentForm
from django.db.models import Q


def home(request):
    return render(request, "blog/base.html")


def posts(request):
    return render(request, "blog/posts.html")


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "blog/login.html"


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        pform = ProfileForm(instance=profile)
    return render(request, "blog/profile.html", {"pform": pform})


# ----------------- POSTS -----------------
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tags_input = form.cleaned_data.get("tags_input", "")
        self._assign_tags(self.object, tags_input)
        return response
    
    def _assign_tags(self, post, tags_input):
        names = [n.strip() for n in tags_input.split(",") if n.strip()]
        tags = []
        for name in names:
            tag, created = Tag.objects.get_or_create(name__iexact=name, defaults={"name": name})
            tags.append(tag)
        post.tags.set(tags) 


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        tags_input = form.cleaned_data.get("tags_input", "")
        self._assign_tags(self.object, tags_input)
        return response

    def _assign_tags(self, post, tags_input):
        names = [n.strip() for n in tags_input.split(",") if n.strip()]
        tags = []
        for name in names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        post.tags.set(tags)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class PostByTagListView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        
        tag_slug = self.kwargs.get("tag_slug")
    
        self.tag = get_object_or_404(Tag, name__iexact=tag_slug)
        return self.tag.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
    
def search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, "blog/search_result.html", {"query": query, "results": results})



# ----------------- COMMENTS -----------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["pk"])
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs["pk"])

    def test_func(self):
        return self.request.user == self.get_object().author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object().post
        return context



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs["pk"])

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})