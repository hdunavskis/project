from typing import Dict, Any, List,Optional
from django.shortcuts import render
from django.http import Http404
from django.core.cache import cache
from django.views.generic import TemplateView, RedirectView
from website.NordClient import ClientSingleton
from website.utils import utils

class HomeView(TemplateView):
    template_name: str = 'index.html'
    http_method_names: List[str] = ['get']
    client = ClientSingleton().client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)
        context["institutions"] = utils.get_institutions(self.client)

        return context

class CreateRequisitionView(RedirectView):
    url: Optional[str] = None
    http_method_names: List[str] = ['get']
    client = ClientSingleton().client

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        created_requisition = utils.create_requisition(self.client,
        self.kwargs.get('institute_id'))
        self.url = created_requisition.get('link')
        return super().get_redirect_url(*args, **kwargs)

class AuthenticateView(TemplateView):
    template_name: str = 'authenticated.html'
    http_method_names: List[str] = ['get']
    client = ClientSingleton().client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        requisition_id = self.kwargs.get('requisition_id') if 'requisition_id' in\
            self.kwargs else self.request.GET.get('ref')

        if requisition_id is not None:
            context['results'] = self._get_accounts(requisition_id)
            context['requisition_id'] = requisition_id
        return context


    def _get_accounts(self, requisition_id):
        accounts = utils.get_accounts(self.client, requisition_id)
        if accounts.get('status') != 'LN':
            raise Http404('Could not retrieve accounts')
        cache_value = cache.get(str(accounts.get('id'))+'accounts')

        if cache_value:
            return cache_value
        cache.set(str(accounts.get('id')+'accounts'), accounts)

        for account in accounts.get('accounts'):
            t_key = str(account) + 'transactions'
            b_key = str(account) + 'balance'
            a_key = str(account) + 'account'
            account_api = self.client.account_api(account)
            try:
                task_transactions = utils.get_tranactions.apply_async(args=[account_api])
                task_balance = utils.get_balance.apply_async(args=[account_api])
                task_accounts = utils.get_account_details.apply_async(args=[account_api])
            except Exception as exc:
                raise Http404('Error gathering premiums!') from exc
            cache.set_many({t_key:task_transactions.get(), b_key:task_balance.get(),
                            a_key:task_accounts.get()})

        return accounts

class TransactionsView(TemplateView):
    template_name: str = 'transactions.html'
    http_method_names: List[str] = ['get']
    client = ClientSingleton().client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        cache_key = str(account_id) + 'transactions'
        context['requisition_id'] = self.kwargs.get('requisition_id')
        context['account_id'] = account_id

        if cache.get(cache_key) is not None:
            context.update(cache.get(cache_key))
            return context

        account_api = self.client.account_api(account_id)
        transactions_results = utils.get_tranactions.apply_async(args=[account_api]).get()
        cache.set(cache_key, transactions_results)
        context.update(transactions_results)

        return context

class BalanceView(TemplateView):
    template_name: str = 'balance.html'
    http_method_names: List[str] = ['get']
    client = ClientSingleton().client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        context['account_id'] = account_id
        context['requisition_id'] = self.kwargs.get('requisition_id')
        cache_key = str(account_id) + 'balance'

        if cache.get(cache_key):
            context.update(cache.get(cache_key))
        else:
            client = ClientSingleton().client
            account_api = client.account_api(account_id)
            balance_results = utils.get_balance.apply_async(args=[account_api]).get()
            cache.set(cache_key, balance_results)
            context.update(balance_results)
        return context

class AccountDetailsView(TemplateView):
    template_name: str = 'account_details.html'
    http_method_names: List[str] = ['get']
    client = ClientSingleton().client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        context['account_id'] = account_id
        context['requisition_id'] = self.kwargs.get('requisition_id')
        cache_key = str(account_id) + 'account'

        if cache.get(cache_key):
            context.update(cache.get(cache_key))
        else:
            client = ClientSingleton().client
            account_api = client.account_api(account_id)
            account = utils.get_account_details.apply_async(args=[account_api]).get()
            context.update(account)
            cache.set(cache_key, account)
        return context


def page_not_found(request, *args, **kwargs):
    """Default error page for demo purposes"""
    context = {}
    context['error_args'] = args if args else ''
    context['error'] = kwargs['exception'] if 'exception' in kwargs else kwargs
    return render(request, '404.html', context)
