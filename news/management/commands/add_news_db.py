import os
from datetime import datetime

import pandas as pd
from django.core.management.base import BaseCommand

from news.models import News


class Command(BaseCommand):
    help = "Loads 5 news items from Fake.csv into the database"

    def handle(self, *args, **options):
        csv_path = os.path.join(os.path.dirname(__file__), 'Fake.csv')
        df = pd.read_csv(csv_path).head(5)

        created_count = 0
        for _, row in df.iterrows():
            headline = row['title']

            if News.objects.filter(headline=headline).exists():
                continue

            date_value = datetime.strptime(row['date'], '%B %d, %Y').date()

            News.objects.create(
                headline=headline,
                body=row['text'],
                date=date_value,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} news added to the database'))
