#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import click
from collections import namedtuple
import os
import sys

from .emoji_uploader import EmojiUploader, UploadFailedException
from .slack_session import (
    NoSuchSubdomainException, InvalidCredentialsException
)

EXIT_CODE_NO_SUCH_SUBDOMAIN = 1
EXIT_CODE_INVALID_CREDENTIALS = 2


FailedUpload = namedtuple('FailedUpload', ['emoji_name', 'error'])


def exit(exit_code, message):
    """
    Echo a message and exit with the specified exit code.
    """
    click.echo(message)
    sys.exit(exit_code)


def create_uploader(subdomain, email, password):
    """
    Initialise an EmojiUploader with the given credentials. This uploader is
    enhanced with a list containing all of its failed uploads.
    """
    try:
        click.echo('\nObtaining cookies and crumbs from Slack...')
        emoji_uploader = EmojiUploader(subdomain, email, password)
    except NoSuchSubdomainException:
        message = 'It looks like the subdomain {subdomain} doesn\'t exist!' \
            .format(subdomain=subdomain)
        exit(EXIT_CODE_NO_SUCH_SUBDOMAIN, message)
    except InvalidCredentialsException:
        message = 'Those credentials appear to be invalid!'
        exit(EXIT_CODE_INVALID_CREDENTIALS, message)

    emoji_uploader.failed_uploads = []
    return emoji_uploader


def get_emoji_name(filename):
    """
    Get the name under which an emoji should be uploaded.
    """
    return os.path.splitext(os.path.basename(filename))[0]


def upload_emoji(emoji_uploader, emoji_name, emoji_file):
    """
    Attempt to upload the given emoji.
    """
    click.echo('Uploading emoji {name}... '.format(name=emoji_name), nl=False)
    try:
        emoji_uploader.upload(emoji_name, emoji_file)
        click.echo(click.style('Done!', fg='green', bold=True))
    except UploadFailedException as e:
        error = str(e)
        click.echo(click.style('Failed! ({error})'.format(error=error),
                               fg='red', bold=True))
        emoji_uploader.failed_uploads.append(FailedUpload(emoji_name, error))


def summarize_results(failed_uploads):
    """
    Display a summary of all failed uploads.
    """
    click.echo('\nAll done!')
    if failed_uploads:
        click.echo('The following emoji could not be uploaded:\n')
        for failure in failed_uploads:
            click.echo('{name}: '.format(name=failure.emoji_name), nl=False)
            click.echo(click.style(failure.error, fg='red', bold=True))


@click.command()
@click.argument('emoji_files', type=click.Path(exists=True), nargs=-1)
@click.option('--subdomain', '-s', type=click.STRING,
              help='Your Slack subdomain',
              prompt='Please enter your Slack subdomain')
@click.option('--email', '-e', type=click.STRING,
              help='Your Slack email address',
              prompt='Please enter your email address')
@click.option('--password', '-p', type=click.STRING,
              help='Your Slack password', hide_input=True,
              prompt='Please enter your password (will not echo)')
def main(emoji_files, subdomain, email, password):
    """
    Upload custom emoji to Slack. Each emoji must conform to Slack's rules:

    \b
      - No more than 128px in width or height
      - No more than 64K in size
    """

    # Start up a session which is authenticated to Slack
    emoji_uploader = create_uploader(subdomain, email, password)

    # Upload each of the given emoji, in turn
    for emoji_file in emoji_files:
        emoji_name = get_emoji_name(emoji_file)
        upload_emoji(emoji_uploader, emoji_name, emoji_file)

    # Output a summary of the run
    summarize_results(emoji_uploader.failed_uploads)


if __name__ == '__main__':
    main()
