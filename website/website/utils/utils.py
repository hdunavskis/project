from enum import Enum
from typing import List
from requests.models import HTTPError
from django.http import Http404
from nordigen import NordigenClient
from nordigen.api import AccountApi
from nordigen.types.types import Requisition, Institutions


class URI(Enum):
    REDIRECT_ADDRESS = 'http://0.0.0.0:8000/authenticated/'


def get_accounts(client:NordigenClient) -> Requisition:
    accounts = None
    try:
        accounts = client.requisition.get_requisition_by_id(client.requisition_id)
    except HTTPError as response:
        raise Http404('Requisition was not created!') from response
        #log error
    return accounts


def create_requisition(client:NordigenClient, institution_id:str) -> Requisition:
    created_req = None
    try:
        created_req = client.requisition.create_requisition(
            redirect_uri=URI.REDIRECT_ADDRESS.value,
            reference_id='',
            institution_id=institution_id
        )
    except HTTPError as response:
        raise Http404('Requisition was not created!') from response
        #log error
    return created_req


def get_institute(client:NordigenClient, institute_id:str) -> Institutions:
    institute = None
    try:
        institute = client.institution.get_institution_by_id(institute_id)
    except HTTPError as response:
        raise Http404('Institution not found') from response
        #log error
    return institute


def get_institutions(client:NordigenClient) -> List[Institutions]:
    institutions = None
    try:
        institutions = client.institution.get_institutions()
    except HTTPError as response:
        raise Http404('Institution not found') from response
        #log error
    return institutions

#celery
def get_tranactions(account_api: AccountApi) -> dict:
    transactions = None
    try:
        transactions = account_api.get_transactions()
    except HTTPError as response:
        raise Http404('Could not get transactions') from response
        #log error
    return transactions

#celery
def get_balance(account_api: AccountApi) -> dict:
    balances = None
    try:
        balances = account_api.get_balances()
    except HTTPError as response:
        raise Http404('Could not get account balances') from response
        #log error
    return balances

#celery
def get_account_details(account_api: AccountApi) -> dict:
    account_details = None
    try:
        account_details = account_api.get_details()
    except HTTPError as response:
        raise Http404('Could not get account details') from response
        #log error
    return account_details
