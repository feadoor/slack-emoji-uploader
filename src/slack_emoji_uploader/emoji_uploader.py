# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup as BSoup
from copy import copy
from requests import codes

from .beautiful_soup_helper import get_input_value
from .slack_session import SlackSession


class EmojiUploader:
    """
    A wrapper around a SlackSession which is responsible for using the session
    to upload custom emoji.
    """

    def __init__(self, subdomain, email, password):
        self.session = SlackSession(subdomain, email, password)
        self._upload_url = _upload_url(subdomain)
        self._base_form_data = self._base_form_data()

    def upload(self, emoji_name, emoji_file):
        """
        Upload an emoji with the given name and filename.
        """

        # POST the upload form data
        form_data = copy(self._base_form_data)
        form_data['name'] = emoji_name
        with open(emoji_file, 'rb') as file:
            files = {'img': file}
            upload = self.session.post(self._upload_url,
                                       data=form_data,
                                       files=files)

        # Checking for a 302 response, rather than a 200, seems to be the most
        # reliable way of determining if the upload succeeded
        if upload.status_code != codes.found:
            raise UploadFailedException()

    def _base_form_data(self):
        """
        Assemble the common form data that will be required for every emoji
        upload, so that it can be reused across multiple requests.
        """
        emoji_page = self.session.get(self._upload_url)
        emoji_form = BSoup(emoji_page.text, 'html.parser').find('form')
        return {
            'add': 1,
            'crumb': get_input_value(emoji_form, 'crumb'),
            'mode': 'data',
        }


def _upload_url(subdomain):
    """
    Returns the URL for the emoji upload page for the given subdomain.
    """
    base_url = 'https://{subdomain}.slack.com/customize/emoji'
    return base_url.format(subdomain=subdomain)


class UploadFailedException(Exception):
    pass
