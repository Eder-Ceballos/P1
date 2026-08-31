import os
import pandas as pd
from django.core.management.base import BaseCommand

from movie.models import Movie

# ruta relativa dentro de MEDIA_ROOT que ya contiene la imagen movie/images/default.jpg
DEFAULT_IMAGE_NAME = 'movie/images/default.jpg'


class Command(BaseCommand):
    help = "Loads movies from movies_initial.csv into the database"

    def handle(self, *args, **options):
        csv_path = os.path.join(os.path.dirname(__file__), 'movies_initial.csv')

        df = pd.read_csv(csv_path)

        created_count = 0
        for _, row in df.iterrows():
            title = row['title']
            genre = row['genre']
            year = int(row['year']) if not pd.isna(row['year']) else None
            description = row['description']

            if Movie.objects.filter(title=title).exists():
                continue

            # todas las peliculas del dataset comparten la misma imagen por defecto
            Movie.objects.create(
                title=title,
                description=description,
                genre=genre,
                year=year,
                image=DEFAULT_IMAGE_NAME,
            )

            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} movies added to the database'))
