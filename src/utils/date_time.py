from datetime import datetime


class DateTime:

    @classmethod
    def current_datetime(cls) -> datetime:
        '''
            Function that calculate the current date time

        Return:
            datetime: the actual date time
        '''
        return datetime.utcnow()
