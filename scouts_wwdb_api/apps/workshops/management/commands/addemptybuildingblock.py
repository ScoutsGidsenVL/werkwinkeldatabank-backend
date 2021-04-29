from django.core.management.base import BaseCommand, CommandError
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from ...models import BuildingBlockTemplate
from ...models.enums import BuildingBlockType


class Command(BaseCommand):
    help = "Adds the empty building block to the database if not exists yet"
    exception = False

    def handle(self, *args, **options):
        template = BuildingBlockTemplate.objects.get_empty_default()
        if not template:
            template = BuildingBlockTemplate(
                title="Empty template",
                description="The empty building block template",
                duration=timedelta(hours=1),
                building_block_type=BuildingBlockType.THEMATIC,
                is_default_empty=True,
                last_edited=timezone.now(),
            )
            template.save()
            self.stdout.write(self.style.SUCCESS("Empty building block template created"))
        else:
            self.stdout.write(self.style.SUCCESS("Empty building block template already existis"))
