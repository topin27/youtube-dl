# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor

import re

class Zhibo8IE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?zhibo8\.cc/\w+/\d+/(?P<id>[0-9a-z-]+)-svideo.htm'
    _TEST = {
        'url': 'https://www.zhibo8.cc/nba/2022/0120-aa44a0b-svideo.htm',
        'md5': 'a753b32ada83137ca584dabf821492b5',
        'info_dict': {
            'id': '0120-aa44a0b',
            'title': '哟呵！实战360度三分投篮太秀了',
            'ext': 'mp4',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')
        video_url = self._search_regex(r'video_url: "(.+?)"', webpage, 'video_url')
        id = re.search(r'https://vodzz.duoduocdn.com/vod-player/(\d+)/(\d+)/.*', video_url)
        json_url = 'https://playvideo.qcloud.com/getplayinfo/v4/{}/{}'.format(id.group(1), id.group(2))
        json_content = self._download_json(json_url, video_id)
        video_url = json_content['videoInfo']['sourceVideo']['url']
        ext = video_url[video_url.rfind('.') + 1 :]
        
        return {
            'id': video_id,
            'title': title,
            'url': video_url,
            'ext': ext,
            # 'description': self._og_search_description(webpage),
            # 'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }
