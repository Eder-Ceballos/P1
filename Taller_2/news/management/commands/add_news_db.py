from django.core.management.base import BaseCommand
from news.models import News
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Load 5 news from Fake.csv into the News model'

    def handle(self, *args, **kwargs):
        csv_file_path = 'news/management/commands/Fake.csv'

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows[:5]:
            headline = row['title']
            exist = News.objects.filter(headline=headline).first()
            if not exist:
                try:
                    date_value = datetime.strptime(
                        row['date'],
                        '%B %d, %Y'
                    ).date()
                    News.objects.create(
                        headline=headline,
                        body=row['text'],
                        date=date_value,
                    )
                except Exception:
                    pass
