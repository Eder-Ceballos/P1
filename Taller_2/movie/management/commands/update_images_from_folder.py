import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Assign previously generated images from media/movie/images/ to each movie"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0
        for movie in movies:
            image_filename = f"m_{movie.title}.png"
            image_path_full = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path_full):
                movie.image = os.path.join('movie/images', image_filename)
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Assigned image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title} ({image_path_full})")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies from folder."))
