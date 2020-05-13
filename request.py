#!/usr/bin/python3

from Pwl import Pwl
from requests import HTTPError
import os

client = Pwl(os.environ.get('url'), os.environ.get('secret'))

# Get account information
#print(client.account_info())

# Get supported languages
#print(client.supported_langs())

# Check order status
#print(client.retrieve_order(1))

# Check order file status
#print(client.retrieve_order_file(1, 1))

print(client.download_order_file(1, 1))


# Full translation process
def translate():
    try:
        # Create an order
        response = client.create_order('test order')
        order_id = response['orderid']

        # Add file to order (binary style)
        response = client.add_xliff_file_to_order(order_id, 'en_US', 'fr_FR', 'Test order file', open('test_file.xlf', 'rb'))
        order_file_id = response['fileid']

        # Add a callback URL to the order 
        client.add_request_callback_to_order(order_id, 'https://powerling.com')

        # Alternative: add a callback URL on the file level
        client.add_request_callback_to_order_file(order_id, order_file_id, 'https://powerling.com')

        # Submit translation order to Powerling team
        client.submit_translation_order(order_id)
    except HTTPError as e:
        print('Error during request: %d %s' % (e.response.status_code, e.response.reason))

#translate()
