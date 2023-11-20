from typing import List, Set

import pandas as pd
from .utils import parse


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance = pd.read_csv(distance_filepath, index_col='id')
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return set(genres)
    
    def get_year(self, title) -> List[str]:
        return self.movies[self.movies['title'] == title]['release_year'].values.astype(int)
    
    def get_overview(self, title) -> List[str]:
        return self.movies[self.movies['title'] == title]['overview'].values

    def recommendation(self, title: str, genre: str = None, year: str = None, top_k: int = 5) -> List[str]:
        if title not in self.movies['title'].values:
            raise ValueError(f"В списке нет фильма '{title}'.") 
         
        movies_filter = self.movies.copy()
        movie_indexes = movies_filter[movies_filter['title'] == title].index
        movie_index = movie_indexes[0]

        movie_cos_sim = pd.DataFrame(self.distance[movie_index])
        movie_cos_sim.columns = ['cosine_sim']
        movies_filter['cosine_sim'] = movie_cos_sim
        if genre:
            movies_filter = movies_filter[movies_filter['genres'].apply(lambda x: genre in x)]

        if year:
            movies_filter.release_year = movies_filter.release_year.fillna(0)
            movies_filter = movies_filter[movies_filter.release_year >= float(year)]
        if movies_filter.empty:
            return []
        elif len(movies_filter) == 0:
            return []     
        else:
            movies_filter.sort_values(['cosine_sim'], ascending=False)[['title', 'cosine_sim']]
            movie_sim_index = movies_filter.sort_values(by='cosine_sim', ascending=False).head(top_k+1).index #.tail(top_k).index
            if movie_index == movie_sim_index[0]:
                movie_sim_index = movie_sim_index[1:]  
            else:
                movie_sim_index = movie_sim_index[:top_k]      
            movie_sim_index = [i for i in movie_sim_index]
            return self.movies.iloc[self.movies.index.isin(movie_sim_index)]['title'].values

           
           

