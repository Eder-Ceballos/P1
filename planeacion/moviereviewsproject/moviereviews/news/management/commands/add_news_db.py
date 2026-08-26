import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from news.models import News

class Command(BaseCommand):
    help = 'Carga noticias desde un archivo CSV a la base de datos'

    def handle(self, *args, **kwargs):
        # Lee el archivo Fake.csv (asegúrate de ubicarlo en la raíz o en la ruta correcta)
        df = pd.read_csv('Fake.csv')
        
        # Tomamos las primeras 5 noticias como pide el taller
        for index, row in df.head(5).iterrows():
            date_value = datetime.strptime(row['date'].strip(), '%B %d, %Y').date()
            
            News.objects.create(
                headline=row['title'],
                body=row['text'],
                date=date_value
            )
            
        self.stdout.write(self.style.SUCCESS('¡Se han cargado las 5 noticias exitosamente desde Fake.csv!'))
