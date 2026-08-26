import csv
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = 'Carga películas desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Ruta del archivo CSV con las películas'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    movie, created = Movie.objects.get_or_create(
                        title=row['title'],
                        defaults={
                            'year': int(row['year']),
                            'genre': row['genre'],
                            'rating': float(row['rating']),
                            'description': row['description'],
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ {row["title"]}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'⚠ Ya existe: {row["title"]}')
                        )
            
            self.stdout.write(self.style.SUCCESS('✓ Carga completa!'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'✗ No encontrado: {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))