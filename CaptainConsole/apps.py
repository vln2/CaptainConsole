from django.apps import AppConfig

from django.db.models.signals import post_migrate

def rebuild_tree(sender, **kwargs):
    from .models import Category
    Category.objects.rebuild()

class CaptainConsoleConfig(AppConfig):
    name = 'CaptainConsole'

    def ready(self):
        post_migrate.connect(rebuild_tree, sender=self)