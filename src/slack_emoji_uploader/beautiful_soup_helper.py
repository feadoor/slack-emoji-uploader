# -*- encoding: utf-8 -*-
"""
Helper functions for extracting useful data from the parsed HTML responses
to the requests that we make to Slack.
"""


def get_input_value(soup, input_name):
    """
    Gets the `value` attribute of the first `input` element whose `name`
    attribute is equal to the given value.
    """
    input_element = soup.find('input', attrs={'name': input_name})
    if input_element is None or not input_element.has_attr('value'):
        return None
    return input_element['value']


def get_page_error(soup):
    """
    Gets the content of a page error that is displayed after an unsuccessful
    request to Slack.
    """
    error = soup.find('p', class_='alert_error')
    return None if error is None else error.get_text()
