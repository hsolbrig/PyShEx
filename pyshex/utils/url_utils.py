from urllib.parse import urlparse, urlunparse, ParseResult

import os


def generate_base(path: str) -> str:
    """ Convert path, which can be a URL or a file path into a base URI

    :param path: file location or url
    :return: file location or url sans actual name
    """
    if ':' in path:
        parts = urlparse(path)
        parts_dict = parts._asdict()
        parts_dict['path'] = os.path.split(parts.path)[0] if '/' in parts.path else ''
        return urlunparse(ParseResult(**parts_dict)) + '/'
    else:
        return (os.path.split(path)[0] if '/' in path else '') + '/'
