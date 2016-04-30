from subfind.model import Subtitle
from subfind.processor import SingleSubtitleProcessor, MultipleSubtitleProcessor
from subfind.utils.subtitle import subtitle_extensions, remove_subtitle, get_subtitle_info
from .exception import MovieNotFound, SubtitleNotFound, ReleaseMissedLangError
from .movie_parser import parse_release_name
from .release.alice import ReleaseScoringAlice
from .scenario import ScenarioManager
from .utils import write_file_content

EVENT_SCAN_RELEASE = 'SCAN_RELEASE'
EVENT_RELEASE_FOUND_LANG = 'RELEASE_FOUND_LANG'
EVENT_RELEASE_COMPLETED = 'RELEASE_COMPLETED'
EVENT_RELEASE_MOVIE_NOT_FOUND = 'RELEASE_MOVIE_NOT_FOUND'
EVENT_RELEASE_SUBTITLE_NOT_FOUND = 'RELEASE_SUBTITLE_NOT_FOUND'


