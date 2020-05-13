import json
import requests

# Handle interactions with Powerling API

class Pwl:
    def __init__(self, uri, auth_token):
        self.uri = uri
        self.auth_token = auth_token

    # Retrieve account information
    def account_info(self):
        return self.__call_api('/account', False)

    # Get supported language couples
    def supported_langs(self):
        return self.__call_api('/supported-langs', False)

    # Create a translation order
    def create_order(self, order_name, duedate = None, metadata = None):
        return self.__call_api('/order/create', True, {'name': order_name, 'duedate': duedate, 'metadata': metadata})

    # Retrieve a translation order status
    def retrieve_order(self, order_id):
        return self.__call_api('/order/%d' % (order_id), False)

    # Retrieve a translation order file status
    def retrieve_order_file(self, order_id, order_file_id):
        return self.__call_api('/order/%d/file/%d/status' % (order_id, order_file_id), False)

    # Download translated file
    def download_order_file(self, order_id, order_file_id):
        return self.__call_api('/order/%d/file/%d' % (order_id, order_file_id), False, None, None, True)

    # Add a binary file to a translation order
    def add_xliff_file_to_order(self, order_id, source_lang, target_lang, client_ref, fil):
        return self.__call_api('/order/%d/upload-file' % (order_id), True, {'sourcelang': source_lang, 'targetlang': target_lang, 'clientref': client_ref}, {'file': fil})

    # Add a file to a translation order using a public URL
    def add_xliff_file_to_order_from_url(self, order_id, source_lang, target_lang, client_ref, file_url):
        return self.__call_api('/order/%d/add-file' % (order_id), True, {'sourcelang': source_lang, 'targetlang': target_lang, 'clientref': client_ref, 'fileurl': file_url})

    # Send the order (trigger translation process at Powerling when all the files are uploaded)
    def submit_translation_order(self, order_id):
        return self.__call_api('/order/%d/submit' % (order_id))

    # Specify a callback URL that will be triggered when the translation is complete
    def add_request_callback_to_order(self, order_id, callback_url):
        return self.__call_api('/order/%d/request-callback' % (order_id), True, {'url': callback_url})

    # Specify a callback URL that will be triggered when translation of a given file is complete
    def add_request_callback_to_order_file(self, order_id, order_file_id, callback_url):
        return self.__call_api('/order/%d/file/%d/request-callback' % (order_id, order_file_id), True, {'url': callback_url})

    def __call_api(self, path, is_post=True, data=None, files=None, binary=False):
        hed = {'Authorization': 'Bearer %s' % (self.auth_token)}
        url = self.uri + path

        if is_post:
            if files is not None:
                # Multipart
                response = requests.post(url, data=data, headers=hed, files=files)
            else:
                # JSON
                response = requests.post(url, json=data, headers=hed)
        else:
            # GET
            response = requests.get(url, json=data, headers=hed)

        # Exceptions on error code
        response.raise_for_status()

        if binary:
            return response.content
        else:
            return response.json()
