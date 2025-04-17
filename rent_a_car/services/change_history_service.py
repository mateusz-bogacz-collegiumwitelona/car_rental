import csv
from typing import List, Dict, Any
from django.http import HttpResponse
from ..models import HistoriaZmian
from ..repositories.change_history_repository import ChangeHistoryRepository

class ChangeHistoryService:
    def __init__(self):
        self.repo = ChangeHistoryRepository

    def get_all_history_change(self) -> List[HistoriaZmian]:
        return self.repo.get_all()
    
    def filter_history_change(self, params: Dict[str, Any]) -> List[HistoriaZmian]:
        return self.repo.filter_by_params(params)
    
    def export_to_csv(self, data: List[HistoriaZmian] = None) -> HttpResponse:
        if data is None:
            data = self.get_all_history_change()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="historia_zmian.csv"'

        response.write(u'\ufeff'.encode('utf8'))
        
        writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        headers = [
            'ID', 'Tabela źródłowa', 'ID rekordu', 'Operacja', 'Data operacji',
            'Miasto', 'Ulica', 'Nr ulicy', 'Kod pocztowy', 'ID użytkownika',
            'Imię', 'Nazwisko', 'PESEL', 'Email', 'ID zamieszkania'
        ]
        writer.writerow(headers)

        for item in data:
            writer.writerow([
                item.id_historii,
                item.tabela_zrodlowa,
                item.id_rekordu,
                item.operacja,
                item.data_operacji,
                item.miasto,
                item.ulica,
                item.nr_ulicy,
                item.kod_pocztowy,
                item.id_user,
                item.imie,
                item.nazwisko,
                item.pesel,
                item.email,
                item.id_zamieszkania
            ])
        
        return response

