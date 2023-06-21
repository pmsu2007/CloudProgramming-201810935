from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from account.models import Account
from home.models import Goal


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            account = Account.objects.create(user=user, balance=0)
            login(request, user)
            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'home/registerPage.html', {'form': form})


class GoalList(ListView):
    model = Goal
    template_name = 'home/homePage.html'
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(GoalList, self).get_context_data()
        if self.request.user.is_authenticated:
            current_user = self.request.user
            current_account = Account.objects.get(user=current_user)

            context['account'] = current_account
            return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user=self.request.user)


class GoalDetail(DetailView):
    model = Goal
    template_name = 'home/goalDetailPage.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        current_account = Account.objects.get(user=current_user)

        context = super(GoalDetail, self).get_context_data()
        context['account'] = current_account
        return context


class GoalCreate(LoginRequiredMixin, CreateView):
    model = Goal
    fields = ['title', 'description', 'amount', 'image']
    template_name = 'home/goalCreatePage.html'

    def form_valid(self, form):
        current_user = self.request.user

        goal = form.save(commit=False)
        goal.user = current_user

        return super(GoalCreate, self).form_valid(form)


class GoalUpdate(UpdateView):
    model = Goal
    fields = ['title', 'description', 'amount', 'image']
    template_name = 'home/goalUpdatePage.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(GoalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        if not form.cleaned_data['image']:
            del form.cleaned_data['image']  # 이미지 필드가 비어 있을 때 삭제
        else:
            form.cleaned_data['image'] = self.get_object().image  # 기존 이미지 할당

        return super().form_valid(form)


class GoalDelete(DeleteView):
    model = Goal
    template_name = 'home/goalDeletePage.html'
    success_url = reverse_lazy('goal_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(GoalDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
