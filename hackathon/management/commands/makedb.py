import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from hackathon.models import Project, Technology


class Command(BaseCommand):
    def handle(self, *args, **options):
        Project.objects.all().delete()
        Technology.objects.all().delete()

        project_dir = os.path.join(settings.PROJECT_ROOT, '..', 'projects')

        i = 0

        for fname in os.listdir(project_dir):
            path = os.path.join(project_dir, fname)
            with open(path, 'r') as f:
                js = json.load(f)

            details = js['details_text'].strip()
            project_id = int(js['id'])
            is_winner = js['is_winner']
            name = js['name'].strip()
            pitch = js['pitch'].strip()
            thumbnail = js['thumbnail'].strip()
            url = js['url'].strip()

            project, created = Project.objects.get_or_create(project_id=project_id, defaults={
                'details': details,
                'is_winner': is_winner,
                'name': name,
                'pitch': pitch,
                'thumbnail': thumbnail,
                'url': url
            })

            for tech_name in js['built_with']:
                tech, created = Technology.objects.get_or_create(name=tech_name)
                tech.save()
                project.technologies.add(tech)

            i += 1
            if i % 100 == 0:
                print(i)
