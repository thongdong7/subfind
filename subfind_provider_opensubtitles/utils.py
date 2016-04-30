def fix_line_ending(content):
    """Fix line ending of `content` by changing it to \n.
    :param bytes content: content of the subtitle.
    :return: the content with fixed line endings.
    :rtype: bytes
    """
    return content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')