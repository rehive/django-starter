from collections import OrderedDict

main = [{'category': 'Basic Information',
         'note': 'Select required fields for this tier.',
         'field': OrderedDict([('first_name', 'First Name'),
                               ('last_name', 'Last Name'),
                               ('nationality', 'Nationality'),
                               ('birth_date', 'Birthdate'),
                               ('id_number', 'ID Number'),
                               ('language', 'Language'),
                               ('address', 'Address'),
                               ('bank_account', 'Bank Account'),
                               ])},
        {'category': 'Account Verification',
         'note': 'Select required verification checks for this tier.',
         'field': OrderedDict([('verified_email_address', 'Verified Email Address'),
                               ('verified_mobile_number', 'Verified Mobile Number'),
                               ('proof_of_identity', 'Verified Proof of Identity'),
                               ('proof_of_address', 'Verified Proof of Address'),
                               ])
         },
        {'category': 'Advanced Account Verification',
         'note': 'Select required advanced verification checks for this tier.',
         'field': OrderedDict([('advanced_proof_of_identity', 'Verified Confirmation ID'), ])}
        ]

template_list = main
