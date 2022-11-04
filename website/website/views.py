from django.shortcuts import render, redirect
from django.http import Http404
from django.views.decorators.http import require_http_methods
from website.NordClient import ClientSingleton
from website.utils import utils


@require_http_methods(['GET'])
def index(request):
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
    context = {}
    client = ClientSingleton().client

    if requisition_id:
        client.requisition_id = requisition_id

    if hasattr(client, 'requisition_id') and not client.requisition_id:
        raise Http404('Requisition id is not set!')

    context['results'] = utils.get_accounts(client)

    return render(request, 'authenticated.html', context)


@require_http_methods(['GET'])
def premium_products(request, account_id):
    context = {}
    client = ClientSingleton().client
    account_api = client.account_api(account_id)
    context.update(utils.get_tranactions(account_api))
    # context.update(utils.get_balance(account_api))
    # context.update(utils.get_account_details(account_api))
    context['account_id'] = account_id
    return render(request, 'premium_products.html', context)


@require_http_methods(['GET'])
def balance(request, account_id):
    #check cache
    context = {}
    client = ClientSingleton().client
    account_api = client.account_api(account_id)
    context.update(utils.get_balance(account_api))
    context['account_id'] = account_id
    return render(request, 'balance.html', context)


@require_http_methods(['GET'])
def account_details(request, account_id):
    #check cache
    context = {}
    client = ClientSingleton().client
    account_api = client.account_api(account_id)
    context.update(utils.get_account_details(account_api))
    context['account_id'] = account_id
    return render(request, 'account_details.html', context)


def page_not_found(request, *args, **kwargs):
    context = {}
    context['error'] = kwargs['exception']
    return render(request, '404.html', context)


def random(request):
    return render(request, 'random.html', context={})
    #redirect straight from url?

#redis + celery
#cache
#test
#redme
#github