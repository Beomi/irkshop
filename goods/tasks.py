'''
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from core.bank import Transaction


@shared_task
def check_payment(by, amount):
    trs = Transaction().get_transact_dic
    for i in trs:
        if str(i['by'])==str(by) and str(i['amount'])==str(amount):
            return True
    return False
'''