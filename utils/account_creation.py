from generate_ratios import generate_profit_ratios
import os
from dotenv import load_dotenv
import requests

# Load Broker API credentials from .env file
load_dotenv()

BROKER_AUTH = os.getenv("alpaca_broker_auth")

def create_account(email, url, headers, payload_template):
    """
    Create an account with a specified email.

    Args:
        email (str): Email address for the account.
        url (str): API endpoint.
        headers (dict): Request headers.
        payload_template (dict): Template for the payload.

    Returns:
        str: Response from the API.
    """
    payload = payload_template.copy()
    payload["contact"]["email_address"] = email

    response = requests.post(url, json=payload, headers=headers)
    return response.text

def main():
    # API setup
    url = "https://broker-api.sandbox.alpaca.markets/v1/accounts"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": BROKER_AUTH
    }

    # Payload template
    payload_template = {
        "contact": {
            "email_address": "john23.doe@example.com",
            "phone_number": "+15556667788",
            "street_address": ["20 N San Mateo Dr"],
            "city": "San Mateo",
            "state": "CA",
            "postal_code": "94401"
        },
        "identity": {
            "tax_id_type": "USA_SSN",
            "given_name": "John",
            "family_name": "Doe",
            "date_of_birth": "1990-01-01",
            "tax_id": "999-99-9990",
            "country_of_citizenship": "USA",
            "country_of_birth": "USA",
            "country_of_tax_residence": "USA",
            "funding_source": ["employment_income"]
        },
        "disclosures": {
            "is_control_person": True,
            "is_affiliated_exchange_or_finra": True,
            "is_politically_exposed": True,
            "immediate_family_exposed": True,
            "employment_status": "employed"
        },
        "agreements": [
            {
                "agreement": "customer_agreement",
                "signed_at": "2019-09-11T18:09:33Z",
                "ip_address": "111.11.11.11"
            }
        ]
    }

    # Generate profit ratios
    max_ratio = 6  # Adjust as needed
    profit_ratios = generate_profit_ratios(max_ratio)

    # Create accounts using profit ratios
    for numerator, denominator in profit_ratios:
        email = f"{numerator}/{denominator}@email.com"
        response = create_account(email, url, headers, payload_template)
        print(f"Created account with email {email}: {response}")

if __name__ == "__main__":
    main()
