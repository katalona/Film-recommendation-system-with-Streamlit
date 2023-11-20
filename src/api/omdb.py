import requests
from typing import Optional, List


class OMDBApi:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"

    def _images_path(self, title: str) -> Optional[str]:
        res = requests.get(self.url, {'t': title, 'apikey': self.api_key}).json()
        if 'Poster' in res:
            return res['Poster']

    def get_posters(self, titles: List[str]) -> List[str]:
        posters = []
        for title in titles:
            path = self._images_path(title)
            if path == 'N/A':
                posters.append('assets/no_poster.jpg')
            elif path:
                posters.append(path)
            else:
                posters.append('assets/no_poster.jpg')

        return posters
