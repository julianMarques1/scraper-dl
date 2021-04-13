from src.movie import Movie
from src.metadata import Metadata
from functools import reduce
from json import dump
from os import getcwd
from os.path import join, isdir
from typing import List


class Scraper(object):
    def scrape(self, urls: List[str]):
        """Parse structured data from a list of pages."""

        movie = reduce(
            lambda movie, another_movie: movie.merge(another_movie),
            [Movie(Metadata(url).get_json_dl()) for url in urls],
        )
        movie = movie.remove_data(
            [
                "@id",
                "dateCreated",
                "dateModified",
                "datePublished",
                "mainEntityOfPage",
                "url",
            ]
        )

        self.save_movie(movie.data)
        return movie

    def save_movie(self, data):
        with open(
            self.create_file_name(data),
            "w",
            encoding="utf8",
        ) as file:
            dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)

    def create_file_name(self, data):
        name = data["name"] if "name" in data.keys() else "Movie"
        if isinstance(name, list):
            name = name[0]

        return join(getcwd(), "data", name + ".json")