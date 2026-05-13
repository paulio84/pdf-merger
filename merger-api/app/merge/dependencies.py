from app.merge.service import MergeService


async def get_merge_service() -> MergeService:
    """
    Dependency provider for MergeService.

    Returns a new instance of MergeService to be injected into the route.
    """
    return MergeService()
