from django.db import models


class Project(models.Model):
    is_winner = models.BooleanField(default=False)
    name = models.CharField(max_length=1000, null=True)
    project_id = models.IntegerField(primary_key=True, unique=True, default=1)
    url = models.URLField(null=True)
    thumbnail = models.URLField(null=True, max_length=400)
    details = models.TextField(null=True)
    pitch = models.TextField(null=True)

    def __repr__(self):
        return self.name + ': ' + ', '.join(str(tech) for tech in self.technologies.all())

    __str__ = __repr__


class Technology(models.Model):
    name = models.CharField(max_length=200, primary_key=True, unique=True)
    projects = models.ManyToManyField(Project, related_name='technologies')

    def __repr__(self):
        return self.name

    __str__ = __repr__
