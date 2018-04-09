# -*- encoding: utf-8 -*-

from requests import codes, Session
from bs4 import BeautifulSoup as BSoup

from .beautiful_soup_helper import get_input_value


class SlackSession(Session):
    """
    Subclasses requests.Session in order to authenticate to Slack when the
    session is opened. This session will then remember the session data
    that is required in order to remain authenticated to Slack.
    """

    def __init__(self, subdomain, email, password):
        super(SlackSession, self).__init__()
        self._log_in_checked(subdomain, email, password)

    def _log_in_checked(self, subdomain, email, password):
        """
        Log in to Slack using the provided credentials.

        Raises NoSuchSubdomainException if the given subdomain doesn't exist.
        Raises InvalidCredentialsException if the credentials are incorrect.
        """

        # POST the login form data
        login_form_data = self._base_form_data(subdomain)
        login_form_data['email'] = email
        login_form_data['password'] = password
        login = self.post(_login_url(subdomain),
                          data=login_form_data,
                          allow_redirects=False)

        # Slack responds with a 302 for a successful login
        if login.status_code != codes.found:
            raise InvalidCredentialsException()

    def _base_form_data(self, subdomain):
        """
        Put together the form data that will be sent as part of the POST
        request used to authenticate to Slack.

        Raises NoSuchSubdomainException if the given subdomain doesn't exist.
        """

        # Grab a copy of the Slack login page
        login_page = self.get(_login_url(subdomain))
        if login_page.status_code != codes.ok:
            raise NoSuchSubdomainException()

        # The form data is populated from hidden inputs in the login form
        login_form = BSoup(login_page.text, 'html.parser').find('form')
        form_data = {
            name: get_input_value(login_form, name)
            for name in ['signin', 'redir', 'crumb']
        }
        form_data['remember'] = 'on'

        return form_data


def _login_url(subdomain):
    """
    Returns the URL for the login page for the given subdomain.
    """
    return 'https://{subdomain}.slack.com/'.format(subdomain=subdomain)


class NoSuchSubdomainException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass
