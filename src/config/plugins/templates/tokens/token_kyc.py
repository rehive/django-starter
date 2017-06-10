main = [{'category': 'Proof of Address',
         'note': 'Select all documents acceptable for proof of address verification.',
         'field': {'utility_bill': 'Utility Bill',
                   'bank_statement': 'Bank Statement',
                   'lease_or_rental_agreement': 'Lease or Rental Agreement',
                   'municipal_rate_and_taxes': 'Municipal Rate and Taxes Invoice',
                   'mortgage_statement': 'Mortgage Statement',
                   'telephone': 'Telephone or Cellular Account',
                   'insurance_policy': 'Insurance Policy Document',
                   'retail_store': 'Statement of Account Issued by a Retail Store'}},
        {'category': 'Proof of Identity',
         'note': 'Select all documents acceptable for proof of identity verification.',
         'field': {'government_id': 'Government Issued ID',
                   'passport': 'Passport',
                   'drivers_license': 'Drivers License'}},
        {'category': 'Advanced Proof of Identity',
         'note': 'Select all documents acceptable for advanced proof of identity verification.',
         'field': {'id_confirmation': 'ID Confirmation Photo'}}]

template_list = main


def choice_list():
    c = []
    for l in main:
        for k, v in l['field'].items():
            c.append([k, v])

    c.append(['other', 'Other'])
    t = tuple(tuple(x) for x in c)
    return t
