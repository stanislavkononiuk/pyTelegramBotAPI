# -*- coding: utf-8 -*-

import requests
from six import string_types
import telebot
from telebot import types

logger = telebot.logger


def _make_request(token, method_name, method='get', params=None, files=None):
    """
    Makes a request to the Telegram API.
    :param token: The bot's API token. (Created with @BotFather)
    :param method_name: Name of the API method to be called. (E.g. 'getUpdates')
    :param method: HTTP method to be used. Defaults to 'get'.
    :param params: Optional parameters. Should be a dictionary with key-value pairs.
    :param files: Optional files.
    :return:
    """
    request_url = telebot.API_URL + 'bot' + token + '/' + method_name
    result = requests.request(method, request_url, params=params, files=files)
    logger.debug(result.text)
    if result.status_code != 200:
        raise ApiException(method_name, result)
    try:
        result_json = result.json()
        if not result_json['ok']:
            raise Exception()
    except:
        raise ApiException(method_name, result)
    return result_json['result']


def get_me(token):
    method_url = 'getMe'
    return _make_request(token, method_url)


def send_message(token, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    :param token:
    :param chat_id:
    :param text:
    :param disable_web_page_preview:
    :param reply_to_message_id:
    :param reply_markup:
    :return:
    """
    method_url = r'sendMessage'
    payload = {'chat_id': str(chat_id), 'text': text}
    if disable_web_page_preview:
        payload['disable_web_page_preview'] = disable_web_page_preview
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def get_updates(token, offset=None, limit=None, timeout=None):
    method_url = r'getUpdates'
    payload = {}
    if offset:
        payload['offset'] = offset
    if limit:
        payload['limit'] = limit
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload)


def get_user_profile_photos(token, user_id, offset=None, limit=None):
    method_url = r'getUserProfilePhotos'
    payload = {'user_id': user_id}
    if offset:
        payload['offset'] = offset
    if limit:
        payload['limit'] = limit
    return _make_request(token, method_url, params=payload)


def forward_message(token, chat_id, from_chat_id, message_id):
    method_url = r'forwardMessage'
    payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    return _make_request(token, method_url, params=payload)


def send_photo(token, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
    method_url = r'sendPhoto'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(photo):
        files = {'photo': photo}
    else:
        payload['photo'] = photo
    if caption:
        payload['caption'] = caption
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_location(token, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
    method_url = r'sendLocation'
    payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def send_chat_action(token, chat_id, action):
    method_url = r'sendChatAction'
    payload = {'chat_id': chat_id, 'action': action}
    return _make_request(token, method_url, params=payload)


def send_data(token, chat_id, data, data_type, reply_to_message_id=None, reply_markup=None):
    method_url = get_method_by_type(data_type)
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(data):
        files = {data_type: data}
    else:
        payload[data_type] = data
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def get_method_by_type(data_type):
    if data_type == 'audio':
        return 'sendAudio'
    if data_type == 'document':
        return 'sendDocument'
    if data_type == 'sticker':
        return 'sendSticker'
    if data_type == 'video':
        return 'sendVideo'


def _convert_markup(markup):
    if isinstance(markup, types.JsonSerializable):
        return markup.to_json()
    return markup


def is_string(var):
    return isinstance(var, string_types)

def is_command(text):
    """
    Checks if `text` is a command. Telegram chat commands start with the '/' character.
    :param text: Text to check.
    :return: True if `text` is a command, else False.
    """
    return text.startswith('/')

def extract_command(text):
    """
    Extracts the command from `text` (minus the '/') if `text` is a command (see is_command).
    If `text` is not a command, this function returns None.

    Examples:
    extract_command('/help'): 'help'
    extract_command('/help@BotName'): 'help'
    extract_command('/search black eyed peas'): 'search'
    extract_command('Good day to you'): None

    :param text: String to extract the command from
    :return: the command if `text` is a command (according to is_command), else None.
    """
    return text.split()[0].split('@')[0][1:] if is_command(text) else None


def split_string(text, chars_per_string):
    """
    Splits one string into multiple strings, with a maximum amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.

    :param text: The text to split
    :param chars_per_string: The number of characters per line the text is split into.
    :return: The splitted text as a list of strings.
    """
    return [text[i:i + chars_per_string] for i in range(0, len(text), chars_per_string)]

class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    """

    def __init__(self, function_name, result):
        super(ApiException, self).__init__('{0} failed. Returned result: {1}'.format(function_name, result))
        self.function_name = function_name
        self.result = result
