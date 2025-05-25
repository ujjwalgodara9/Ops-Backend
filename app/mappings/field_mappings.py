# app/mappings/field_mappings.py

# Define field mappings for each image type
EXPECTED_FIELDS = {
    "user_name": "Company Name",
    "user_id": "MFID",
    "bureau_name": "Bank Bureau Name",
    "amt_limit_in_figures": "Amount Limit in Figures",
    "amt_limit_in_words": "Amount Limit in Words",
    "limit_frequency": "Limit Frequency",
    "period_ending": "Period Ending",
    "drawing_account_name": "Drawing Account Name",
    "bsb": "BSB Number",
    "account_number": "Account Number",
    "temporary_processing_limit_override": "Temporary Processing Limit Override"
}

UI_FIELDS = [
    "Company Name",
    "MFID",
    "Bank Bureau Name",
    "Amount Limit in Figures",
    "Amount Limit in Words",
    "Limit Frequency",
    "Period Ending",
    "Drawing Account Name",
    "BSB Number",
    "Account Number",
    "Temporary Processing Limit Override"
]

MAPPING_IMG1 = {
    "Company name (User name)": "user_name",
    "MFID": "user_id",
    "Lodging party (Other Bank Bureau name)": "bureau_name",
    "Maximum total value of entries per processing cycle (Non Cumulative - not including charges)": "amt_limit_in_figures",
    "Amount in words": "amt_limit_in_words",
    "Processing cycle covering maximum peak value": "limit_frequency",
    "Period ending": "period_ending",
    "Name of Account to be debited for payments": "drawing_account_name",
    "BSB no.": "bsb",
    "Account no.": "account_number",
    "Temporary processing limit override": "temporary_processing_limit_override"
}

MAPPING_IMG2 = {
    "User name": "user_name",
    "User ID number": "user_id",
    "Bureau name": "bureau_name",
    "Processing limit": "amt_limit_in_figures",
    "Processing limit under letter-container div": "amt_limit_in_words",
    "Limit frequency": "limit_frequency",
    "Period ending": "period_ending",
    "Account nominated for drawings": "drawing_account_name",
    "BSB Number": "bsb",
    "Account Number": "account_number"
}

MAPPING_IMG3 = {
    "DE User Name": "user_name",
    "DE User ID": "user_id",
    "Via Bureau": "bureau_name",
    "Processing limit amount in brackets": "amt_limit_in_figures",
    "Processing limit amount": "amt_limit_in_words",
    "Limit frequency": "limit_frequency",
    "Period ending": "period_ending",
    "Drawing account name": "drawing_account_name",
    "BSB": "bsb",
    "Account number": "account_number",
    "Temporary processing limit override": "temporary_processing_limit_override"
}

MAPPINGS_BY_TYPE = {
    "desna": MAPPING_IMG1,
    "tna1": MAPPING_IMG2,
    "auspaynet": MAPPING_IMG3
}


# # app/mappings/trust_mappings.py
# TRUST_FIELD_MAPPINGS = {
#     "type_of_trust": [
#         "Type of Trust",
#         "Name of trust",
#         "Trust Type"
#     ],
#     "trustees": [
#         "Trustee/s Name",
#         "Trustee",
#         "Trustees"
#     ],
#     "trustee_address": [
#         "Trustee/s Address",
#         "Trustee Address"
#     ],
#     "beneficiaries": [
#         "Beneficiary/s Name",
#         "Initial Subscribers",
#         "Beneficiaries"
#     ],
#     "beneficiary_addresses": [
#         "Beneficiary/s Address",
#         "Subscriber Address"
#     ],
#     "abn": [
#         "ABN of Trust",
#         "Trust ABN"
#     ],
#     "date_executed": [
#         "Date Trust Executed",
#         "Date of deed"
#     ],
#     "settlor_name": [
#         "Settlor Name"
#     ],
#     "settled_sum": [
#         "Settled Sum $",
#         "Value of the Initial Units"
#     ],
#     "governing_state": [
#         "Governing State",
#         "Governing state"
#     ],
#     "unit_holders": [
#         "Initial Subscriptions",
#         "Unit Holders"
#     ]
# }

# Global trust mapping (what all documents should conform to)
GLOBAL_TRUST_MAPPING = {
    "trust_type": "Type of Trust",
    "trustees": "Trustees",
    "trustee_address": "Trustee Address",
    "beneficiaries": "Beneficiaries",
    "date_executed": "Date Executed",
    "settled_sum": "Settled Sum",
    "governing_state": "Governing State",
    "unit_holders": "Unit Holders"
}

# Document-specific mappings
TRUST_MAPPINGS_BY_TYPE = {
    "online": {
        "Type of Trust:": "trust_type",
        "Trustee/s Name:": "trustees",
        "Trustee/s Address:": "trustee_address",
        "Beneficiary/s Name:": "beneficiaries",
        "Date Trust Executed:": "date_executed",
        "Settled Sum $:": "settled_sum",
        "Governing State:": "governing_state",
        "Initial Subscriptions:": "unit_holders"
    },
    "schedule": {
        "Name of trust": "trust_type",
        "Trustee": "trustees",
        "Trustee Address": "trustee_address",
        "Initial Subscribers": "beneficiaries",
        "Date of deed": "date_executed",
        "Value of the Initial Units": "settled_sum",
        "Governing state": "governing_state",
        "Initial Subscriptions": "unit_holders"
    }
}