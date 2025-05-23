from src.main.infra.utils.log_utils import log
from src.main.domain.event_model import EventDTO
from src.main.business.filter.event_filter_i import EventFilterI
from src.main.business.filter.week_event_filter_impl import WeekEventFilterImpl
from src.main.business.filter.month_event_filter_impl import MonthEventFilterImpl


class EventService:
    def __init__(self):
        self.__filter_week: EventFilterI = WeekEventFilterImpl()
        self.__filter_month: EventFilterI = MonthEventFilterImpl()
        log.info('Constructor - %s', self)

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(filter_week='{self.__filter_week.__class__.__name__}', "
            f"filter_month='{self.__filter_month.__class__.__name__}')"
        )

    def filter_week(self, events: list[EventDTO]) -> list[EventDTO]:
        log.info('%s - filter week input: %s', self.__class__.__name__, events)
        
        events = self.__filter_week.filter_events(events)
        log.info('%s - filter week output: %s', self.__class__.__name__, events)
        return events
    
    def filter_month(self, events: list[EventDTO]) -> list[EventDTO]:
        log.info('%s - filter month input: %s', self.__class__.__name__, events)
        
        events = self.__filter_month.filter_events(events)
        log.info('%s - filter month output: %s', self.__class__.__name__, events)
        return events

