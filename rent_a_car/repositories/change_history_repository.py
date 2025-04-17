from typing import List, Optional, Dict, Any
from django.db.models import Q
from ..models import HistoriaZmian

class ChangeHistoryRepository:
    @staticmethod
    def get_all()->List[HistoriaZmian]:
        return HistoriaZmian.objects.all()
    
    @staticmethod
    def filter_by_params(params: Dict[str, Any]) -> List[HistoriaZmian]:
        query = Q()

        for key, value in params.items():
            if value and hasattr(HistoriaZmian, key):
                query &= Q(**{key: value})

        if not query:
            return HistoriaZmian.objects.all()
        
        return HistoriaZmian.objects.filter(query)