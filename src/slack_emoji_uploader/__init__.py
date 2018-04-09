#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import click
import os
import sys

from .emoji_uploader import EmojiUploader, UploadFailedException
from .slack_session import (
    NoSuchSubdomainException, InvalidCredentialsException
)

EXIT_CODE_NO_SUCH_SUBDOMAIN = 1
EXIT_CODE_INVALID_CREDENTIALS = 2


def exit(exit_code, message):
    click.echo(message)
    sys.exit(exit_code)


def get_emoji_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]


@click.command()
@click.argument('emoji_files', type=click.Path(exists=True),
                nargs=-1, required=True)
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
    try:
        click.echo('Obtaining cookies and crumbs from Slack...')
        emoji_uploader = EmojiUploader(subdomain, email, password)
    except NoSuchSubdomainException:
        message = 'It looks like the subdomain {subdomain} doesn\'t exist!' \
            .format(subdomain=subdomain)
        exit(EXIT_CODE_NO_SUCH_SUBDOMAIN, message)
    except InvalidCredentialsException:
        message = 'Those credentials appear to be invalid!'
        exit(EXIT_CODE_INVALID_CREDENTIALS, message)

    # Upload each of the given emoji, in turn
    failed_uploads = []
    for emoji_file in emoji_files:
        name = get_emoji_name(emoji_file)
        click.echo('Uploading emoji {name}... '.format(name=name), nl=False)
        try:
            emoji_uploader.upload(name, emoji_file)
            click.echo(click.style('Done!', fg='green', bold=True))
        except UploadFailedException:
            click.echo(click.style('Failed', fg='red', bold=True))
            failed_uploads.append(name)

    # Output a summary of failures
    click.echo('All done!')
    if failed_uploads:
        click.echo('The following emoji could not be uploaded')
        click.echo(str(failed_uploads))


if __name__ == '__main__':
    main()
