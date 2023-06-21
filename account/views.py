from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from account.models import Account, Transaction


class TransactionList(ListView):
    model = Transaction
    template_name = 'account/accountPage.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super(TransactionList, self).get_context_data()
        if self.request.user.is_authenticated:
            current_user = self.request.user
            current_account = Account.objects.get(user=current_user)
            current_transaction = Transaction.objects.filter(account=current_account)

            context['balance'] = current_account.balance
            context['income'] = current_transaction.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum']
            context['expense'] = current_transaction.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum']
            return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super().get_queryset().filter(user=self.request.user)
            type_param = self.request.GET.get('type')
            sort_param = self.request.GET.get('sort')

            if type_param:
                queryset = queryset.filter(type=type_param)
            # 최신순 정렬
            elif sort_param == 'asc':
                queryset = queryset.order_by('-date')
            # 과거순 정렬
            elif sort_param == 'desc':
                queryset = queryset.order_by('date')

            return queryset


class TransactionDetail(DetailView):
    model = Transaction
    template_name = 'account/accountDetailPage.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        current_account = Account.objects.get(user=current_user)

        context = super(TransactionDetail, self).get_context_data()
        context['balance'] = current_account.balance
        return context


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['type', 'title', 'description', 'date', 'amount']
    template_name = 'account/accountCreatePage.html'

    def form_valid(self, form):
        current_user = self.request.user
        current_account = Account.objects.get(user=current_user)

        if form.cleaned_data['type'] == 'EXPENSE':
            current_account.balance -= form.cleaned_data['amount']
        elif form.cleaned_data['type'] == 'INCOME':
            current_account.balance += form.cleaned_data['amount']
        current_account.save()

        transaction = form.save(commit=False)
        transaction.account = current_account
        transaction.user = current_user

        return super(TransactionCreate, self).form_valid(form)


class TransactionUpdate(UpdateView):
    model = Transaction
    fields = ['title', 'description', 'date', 'amount']
    template_name = 'account/accountUpdatePage.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(TransactionUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        current_transaction = self.get_object()
        prev_amount = current_transaction.amount

        response = super().form_valid(form)

        current_account = current_transaction.account
        current_account.balance -= prev_amount
        current_account.balance += form.cleaned_data['amount']
        current_account.save()

        return response


class TransactionDelete(DeleteView):
    model = Transaction
    template_name = 'account/accountDeletePage.html'
    success_url = reverse_lazy('transaction_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(TransactionDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def delete(self, request, *args, **kwargs):

        current_transaction = self.get_object()
        current_account = current_transaction.account
        current_account.balance -= current_transaction.amount
        current_account.save()

        return super().delete(request, *args, **kwargs)