import logging
import socket
import zlib

from six.moves.xmlrpc_client import SafeTransport
from six.moves.xmlrpc_client import ServerProxy

import base64
import re
from babelfish import Language
from subfind.provider import BaseProvider
from subfind.exception import ReleaseNotMatchError, MovieNotFound
from subfind.model import Subtitle
from subfind.release import ReleaseMatchingChecker
from subfind.release.alice import ReleaseScoringAlice
from subfind.scenario import BaseScenarioFactory, Scenario1
from subfind_provider_opensubtitles.utils import fix_line_ending


class OpensubtitlesFactory(BaseScenarioFactory):
    def get_scenario(self):
        release_scoring = ReleaseScoringAlice()
        provider = OpensubtitlesProvider()

        return Scenario1(release_scoring, provider)


class TimeoutSafeTransport(SafeTransport):
    """Timeout support for ``xmlrpc.client.SafeTransport``."""

    def __init__(self, timeout, *args, **kwargs):
        SafeTransport.__init__(self, *args, **kwargs)
        self.timeout = timeout

    def make_connection(self, host):
        c = SafeTransport.make_connection(self, host)
        c.timeout = self.timeout

        return c


class OpensubtitlesProvider(BaseProvider):
    def __init__(self):
        self.movie_title_year_pattern = re.compile('^(.*)(\s+\((\d+)\))$')
        self.sub_extensions = ['srt', 'sub', 'ass']
        self.logger = logging.getLogger(self.__class__.__name__)

        self.server = None
        self.token = None

    def _ensure_login(self):
        """
        Ensure that the server is opened
        :return:
        :rtype:
        """
        if self.server is None:
            self.server = ServerProxy('https://api.opensubtitles.org/xml-rpc', TimeoutSafeTransport(100))

            self.logger.info('Logging in')
            response = checked(self.server.LogIn('', '', 'eng', 'subfind v1'))
            self.token = response['token']
            self.logger.debug('Logged in with token %r', self.token)

    def get_sub(self, release):
        sub_id = int(release['IDSubtitleFile'])

        self.logger.info('Downloading subtitle %r', sub_id)
        response = checked(self.server.DownloadSubtitles(self.token, [sub_id]))
        # pprint(response)
        content = fix_line_ending(zlib.decompress(base64.b64decode(response['data'][0]['data']), 47))
        # desc_sub_file = join(target_folder, '%s.%s.%s' % (release_name, release['lang'], release['SubFormat']))
        # write_file_content(desc_sub_file, content)

        return Subtitle(content=content, extension=release['SubFormat'])

    def get_releases(self, release_name, langs):
        self._ensure_login()

        release_matching_checker = ReleaseMatchingChecker(release_name)

        criteria = [
            {'query': release_name}
        ]

        for i in range(5):
            try:
                response = self.server.SearchSubtitles(self.token, criteria)
                break
            except socket.timeout:
                print('socket timeout, try again')
                continue

        checked(response)
        # pprint(response)

        ret = {}
        if response and 'data' in response:
            for subtitle_item in response['data']:
                try:
                    opensubtitle_lang = subtitle_item['SubLanguageID']
                    release_lang = str(Language.fromopensubtitles(opensubtitle_lang).alpha2)
                except:
                    # Exception when
                    continue

                # Ignore not match language
                if release_lang not in langs:
                    continue

                if release_lang not in ret:
                    ret[release_lang] = []

                item_release_name = subtitle_item['MovieReleaseName']
                try:
                    release_matching_checker.check(item_release_name)
                except (ReleaseNotMatchError, MovieNotFound):
                    continue

                release = {
                    'name': item_release_name,
                    'lang': release_lang,
                    'IDSubtitleFile': subtitle_item['IDSubtitleFile'],
                    'SubFormat': subtitle_item['SubFormat']
                }
                ret[release_lang].append(release)

        return ret


class ProviderError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class DownloadLimitExceeded(Exception):
    pass


class OpenSubtitlesError(ProviderError):
    """Base class for non-generic :class:`OpenSubtitlesProvider` exceptions."""
    pass


class Unauthorized(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '401 Unauthorized'."""
    pass


class NoSession(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '406 No session'."""
    pass


class DownloadLimitReached(OpenSubtitlesError, DownloadLimitExceeded):
    """Exception raised when status is '407 Download limit reached'."""
    pass


class InvalidImdbid(OpenSubtitlesError):
    """Exception raised when status is '413 Invalid ImdbID'."""
    pass


class UnknownUserAgent(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '414 Unknown User Agent'."""
    pass


class DisabledUserAgent(OpenSubtitlesError, AuthenticationError):
    """Exception raised when status is '415 Disabled user agent'."""
    pass


class ServiceUnavailable(OpenSubtitlesError):
    """Exception raised when status is '503 Service Unavailable'."""
    pass


def checked(response):
    """Check a response status before returning it.
    :param response: a response from a XMLRPC call to OpenSubtitles.
    :return: the response.
    :raise: :class:`OpenSubtitlesError`
    """
    status_code = int(response['status'][:3])
    if status_code == 401:
        raise Unauthorized
    if status_code == 406:
        raise NoSession
    if status_code == 407:
        raise DownloadLimitReached
    if status_code == 413:
        raise InvalidImdbid
    if status_code == 414:
        raise UnknownUserAgent
    if status_code == 415:
        raise DisabledUserAgent
    if status_code == 503:
        raise ServiceUnavailable
    if status_code != 200:
        raise OpenSubtitlesError(response['status'])

    return response
