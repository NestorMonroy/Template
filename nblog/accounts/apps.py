from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    label = 'blogaccounts'


default_app_config = 'accounts.AccountsConfig'
