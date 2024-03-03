from ..models import BuildingBlockTemplate, History, Workshop


def history_create(*, data: dict, workshop: Workshop = None, building_block: BuildingBlockTemplate = None) -> History:
    history = History(
        data=data,
        workshop=workshop,
        building_block=building_block,
    )
    history.full_clean()
    history.save()

    return history
