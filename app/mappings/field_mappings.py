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
