from subfind.subtitle import SubtitleScoring
from subfind.tokenizer import tokenizer


class SubtitleScoringAlice(SubtitleScoring):
    def sort(self, movie, params, subtitles):
        subtitle_match_tokens = set(params['release_name_tokens'])

        for subtitle in subtitles:
            tmp1 = set(tokenizer(subtitle['name']))
            d = len(subtitle_match_tokens.intersection(tmp1)) * 100 - len(tmp1)

            subtitle['d'] = d

        subtitles.sort(key=lambda sub: -sub['d'])

        return subtitles
