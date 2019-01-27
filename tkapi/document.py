import requests

import tkapi
from tkapi.util import util


class DocumentFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "Datum ge " + util.datetime_to_odata(start_datetime)
        self._filters.append(filter_str)
        filter_str = "Datum lt " + util.datetime_to_odata(end_datetime)
        self._filters.append(filter_str)

    def filter_empty_agendapunt(self):
        filter_str = 'Agendapunt/any(a: true)'
        self._filters.append(filter_str)

    def filter_onderwerp(self, onderwerp):
        filter_str = 'Onderwerp eq ' + "'" + onderwerp.replace("'", "''") + "'"
        self._filters.append(filter_str)

    def filter_titel(self, titel):
        filter_str = 'Titel eq ' + "'" + titel.replace("'", "''") + "'"
        self._filters.append(filter_str)

    def filter_dossier(self, nummer):
        filter_str = "Kamerstukdossier/any(d: d/Nummer eq {})".format(nummer)
        self._filters.append(filter_str)


class Document(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Document'
    orderby_param = 'Datum'

    @staticmethod
    def create_filter():
        return DocumentFilter()

    @property
    def activiteiten(self):
        from tkapi.activiteit import Activiteit
        return self.related_items(Activiteit)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def agendapunten(self):
        agendapunten = []
        for zaak in self.zaken:
            agendapunten += zaak.agendapunten
        return agendapunten

    @property
    def dossiers(self):
        if self.kamerstuk:
            return self.kamerstuk.dossiers
        return []

    @property
    def aanhangselnummer(self):
        return self.get_property_or_empty_string('Aanhangselnummer')

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def datum(self):
        return self.get_date_from_datetime_or_none('Datum')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')

    @property
    def alias(self):
        return self.get_property_or_empty_string('Alias')

    @staticmethod
    def begin_date_key():
        return 'Datum'

    @property
    def dossier_nummer(self):
        if self.kamerstuk and self.kamerstuk.dossier and self.kamerstuk.dossier.nummer:
            return self.kamerstuk.dossier.nummer
        return None

    @property
    def dossier_toevoeging(self):
        if self.kamerstuk and self.kamerstuk.dossier and self.kamerstuk.dossier.toevoeging:
            return self.kamerstuk.dossier.toevoeging
        return None


class VerslagAlgemeenOverleg(Document):
    filter_param = "Soort eq 'Verslag van een algemeen overleg'"

    # @property
    # def commissie(self):
    #     if self.zaak and self.zaak['Voortouwcommissie']:
    #         for commissie in self.zaak['Voortouwcommissie']:
    #             print(commissie['Commissie'])
    #         return self.zaak['Voortouwcommissie'][0]['Commissie']
    #     return None
    #
    # @property
    # def volgcommissie(self):
    #     if self.activiteit and self.activiteit['Volgcommissie']:
    #         return self.activiteit['Volgcommissie'][0]['Commissie']
    #     return None

    @property
    def document_url(self):
        url = ''
        if self.dossiers:
            dossier = self.dossiers[0]
            kamerstuk_id = str(dossier.nummer)
            if dossier.toevoeging and '(' not in dossier.toevoeging:
                kamerstuk_id += '-' + str(dossier.toevoeging)
            kamerstuk_id += '-' + str(self.kamerstuk.ondernummer)
            url = 'https://zoek.officielebekendmakingen.nl/kst-' + kamerstuk_id
            response = requests.get(url, timeout=60)
            assert response.status_code == 200
            if 'Errors/404.htm' in response.url:
                print('WARNING: no verslag document url found')
                url = ''
        else:
            print('no dossier or kamerstuk found')
        return url
