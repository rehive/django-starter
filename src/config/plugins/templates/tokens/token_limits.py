main = [{'category': 'Transfer Limits',
         'field': [{'name': 'tx_transfer_min',
                    'title': 'Minimum amount a user can transfer per transaction',
                    'note': 'Default is set to zero.'},
                   {'name': 'tx_transfer_max_day',
                    'title': 'Maximum total amount a user can transfer per day',
                    'note': 'Default is set to unlimited.'},
                   {'name': 'tx_transfer_max_month',
                    'title': 'Maximum total amount a user can transfer per month',
                    'note': 'Default is set to unlimited.'}]},
        {'category': 'Withdrawal Limits',
         'field': [{'name': 'tx_withdraw_min',
                    'title': 'Minimum amount a user can withdraw per transaction',
                    'note': 'Default is set to zero.'},
                   {'name': 'tx_withdraw_max_day',
                    'title': 'Maximum total amount a user can withdraw per day',
                    'note': 'Default is set to unlimited.'},
                   {'name': 'tx_withdraw_max_month',
                    'title': 'Maximum total amount a user can withdraw per month',
                    'note': 'Default is set to unlimited.'}]},
        {'category': 'Deposit Limits',
         'field': [{'name': 'tx_deposit_min',
                    'title': 'Minimum amount a user can deposit per transaction',
                    'note': 'Default is set to zero.'},
                   {'name': 'tx_deposit_max_day',
                    'title': 'Maximum amount a user can deposit per day',
                    'note': 'Default is set to unlimited.'},
                   {'name': 'tx_deposit_max_month',
                    'title': 'Maximum amount a user can deposit per month',
                    'note': 'Default is set to unlimited.'},
                   ]}]

template_list = main


def choice_list():
    c = []
    for l in main:
        for i in l['field']:
            c.append([i['name'], i['name']])

    t = tuple(tuple(x) for x in c)
    return t
