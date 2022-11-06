from django.shortcuts import render, redirect
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from website.NordClient import ClientSingleton
from website.utils import utils


@require_http_methods(['GET'])
def index(request):
    """
    Index page
    Returns:
        dict: All institutions
    """
    context={}
    client = ClientSingleton().client
    context["institutions"] = utils.get_institutions(client)

    return render(request, 'index.html', context)


@require_http_methods(['GET'])
def requisition_create(request, institute_id):
    client = ClientSingleton().client
    created_requisition = utils.create_requisition(client, institute_id)
    requisition_id = created_requisition.get('id')
    client.requisition_id = requisition_id

    return redirect(created_requisition.get('link'))


@require_http_methods(['GET'])
def authenticated(request, requisition_id=''):
    """Page user is redirected after authentication.
        If authentication was successfull, premium products
        (transactions, accounts, balances) are gathered async.
        Else http404 is raised

        Parameters:
            requisition_id (str): Optional
        Returns:
            dict: Of available accounts
    """
    context = {}
    client = ClientSingleton().client
    accounts = utils.get_accounts(client)
    if cache.get(str(accounts.get('id'))+'accounts'):
        context['results'] = cache.get(str(accounts.get('id'))+'accounts')
    else:
        cache.set(str(accounts.get('id'))+'accounts', accounts)

        if requisition_id:
            client.requisition_id = requisition_id

        elif hasattr(client, 'requisition_id') and not client.requisition_id:
            raise Http404('Requisition id is not set!')

        if accounts.get('status') != 'LN':
            raise Http404('No accounts found! Authentication failed.')

        for account in accounts.get('accounts'):
            t_key = str(account) + 'transactions'
            b_key = str(account) + 'balance'
            a_key = str(account) + 'account'
            account_api = client.account_api(account)
            try:
                transactions_results = utils.get_tranactions.apply_async(args=[account_api]).get()
                balance_results = utils.get_balance.apply_async(args=[account_api]).get()
                accounts_results = utils.get_account_details.apply_async(args=[account_api]).get()
            except Exception as exc:
                raise Http404('Error gathering premiums!') from exc
            cache.set_many({t_key:transactions_results, b_key:balance_results,
                            a_key:accounts_results})

        context['results'] = accounts
    return render(request, 'authenticated.html', context)


@require_http_methods(['GET'])
def transactions(request, account_id):
    """Get transactions async
        Parameters:
            account_id: (str)
        Returns:
            dict: Of all transactions for a given accout
    """
    cache_key = str(account_id) + 'transactions'
    context = {}
    if cache.get(cache_key):
        context.update(cache.get(cache_key))
    else:
        client = ClientSingleton().client
        account_api = client.account_api(account_id)
        transactions_results = utils.get_tranactions.apply_async(args=[account_api]).get()
        cache.set(cache_key, transactions_results)
        context.update(transactions_results)
    context['account_id'] = account_id
    return render(request, 'transactions.html', context)


@require_http_methods(['GET'])
def balance(request, account_id):
    """Get balance async
        Parameters:
            account_id: (str)
        Returns:
            dict: Balance for a given account
    """
    cache_key = str(account_id) + 'balance'
    context = {}
    if cache.get(cache_key):
        context.update(cache.get(cache_key))
    else:
        client = ClientSingleton().client
        account_api = client.account_api(account_id)
        balance_results = utils.get_balance.apply_async(args=[account_api]).get()
        cache.set(cache_key, balance_results)
        context.update(balance_results)
    context['account_id'] = account_id
    return render(request, 'balance.html', context)


@require_http_methods(['GET'])
def account_details(request, account_id):
    """Get account details async
        Parameters:
            account_id: (str)
        Returns:
            dict: Of account details for a given account
    """
    cache_key = str(account_id) + 'account'
    context = {}
    if cache.get(cache_key):
        context.update(cache.get(cache_key))
    else:
        client = ClientSingleton().client
        account_api = client.account_api(account_id)
        account = utils.get_account_details.apply_async(args=[account_api]).get()
        context.update(account)
        cache.set(cache_key, account)
    context['account_id'] = account_id
    return render(request, 'account_details.html', context)


def page_not_found(request, *args, **kwargs):
    """Default error page for demo purposes"""
    context = {}
    context['error_args'] = args if args else ''
    context['error'] = kwargs['exception'] if 'exception' in kwargs else kwargs
    return render(request, '404.html', context)
