"""apps.workshops.management.commands.addemptybuildingblock."""
import datetime as dt

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.workshops.models import BuildingBlockTemplate
from apps.workshops.models.enums import BuildingBlockType


class Command(BaseCommand):
    help = "Adds the empty building block to the database if not exists yet"
    exception = False

    def handle(self, *args, **options):
        template = BuildingBlockTemplate.objects.get_empty_default()

        if template:
            self.stdout.write(self.style.SUCCESS("Empty building block template already existis"))
            return

        template = BuildingBlockTemplate(
            title="Empty template",
            description="The empty building block template",
            duration=dt.timedelta(hours=1),
            building_block_type=BuildingBlockType.THEMATIC,
            is_default_empty=True,
            last_edited=timezone.now(),
        )
        template.save()
        self.stdout.write(self.style.SUCCESS("Empty building block template created"))
