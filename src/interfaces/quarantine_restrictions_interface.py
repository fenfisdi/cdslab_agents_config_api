from src.models.db.master.quarantine_restriction import QuarantineRestriction


class QuarantineRestrictionInterface:
    """
    Interface to consult QuarantineRestrictions in db
    """

    @staticmethod
    def find_all():
        """
        Find all QuarantineRestrictions in db
        """
        return QuarantineRestriction.objects().all()
