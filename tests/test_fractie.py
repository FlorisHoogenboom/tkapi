import datetime

from tkapi.fractie import Fractie, FractieZetel
from tkapi.fractie import FractieZetelPersoon
from tkapi.fractie import FractieZetelVacature
from tkapi.fractie import FractieZetelVacatureSoort

from .core import TKApiTestCase


class TestFractie(TKApiTestCase):
    # start_datetime = datetime.datetime(year=2017, month=1, day=1)
    # end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_fractie(self):
        fractie = self.api.get_item(Fractie, id='8fd1a907-0355-4d27-8dc1-fd5a531b471e')
        print('fractie:', fractie.naam)
        self.assertEqual('GroenLinks', fractie.naam)
        self.assertEqual('GL', fractie.afkorting)
        self.assertEqual(datetime.date(year=1990, month=11, day=24), fractie.datum_actief)
        self.assertEqual(None, fractie.datum_inactief)
        # fractie.print_json()
        leden = fractie.leden_actief
        print('fractieleden:', len(leden))
        self.assertGreaterEqual(len(leden), 14)

    def test_get_fracties(self):
        fracties = self.api.get_fracties(max_items=50)
        for fractie in fracties:
            # fractie.print_json()
            print('id', fractie.id, 'fractie:', fractie.naam, '| zetels:', fractie.zetels_aantal)
        self.assertEqual(41, len(fracties))

    def test_filter_fracties_actief(self):
        filter = Fractie.create_filter()
        filter.filter_actief()
        fracties = self.api.get_fracties(max_items=50, filter=filter)
        for fractie in fracties:
            # fractie.print_json()
            print('fractie:', fractie.naam, '| zetels:', fractie.zetels_aantal)
        # TODO: this will change if current fracties change
        self.assertEqual(15, len(fracties))

    def test_filter_actieve_leden(self):
        filter = Fractie.create_filter()
        filter.filter_fractie('GroenLinks')
        fractie = self.api.get_items(Fractie, filter=filter)[0]
        leden_actief = fractie.leden_actief
        print(fractie.naam, fractie.zetels_aantal)
        # for lid in leden_actief:
        #     print('\t', lid.persoon)
        self.assertEqual(fractie.zetels_aantal, len(leden_actief))


class TestFractieZetel(TKApiTestCase):

    def test_get_fractie_zetels(self):
        zetels = self.api.get_fractie_zetels(max_items=10)
        self.assertEqual(10, len(zetels))
        for zetel in zetels:
            if zetel.fractie_zetel_persoon:
                persoon = zetel.fractie_zetel_persoon.persoon
                print(persoon.voornamen, persoon.achternaam)
            # else:
            #     self.assertTrue(lid.vacature)

    def test_filter_fractie(self):
        filter = FractieZetel.create_filter()
        filter.filter_fractie('GroenLinks')
        zetels = self.api.get_items(FractieZetel, filter)
        self.assertEqual(48, len(zetels))

    # TODO BR: move to fractie_zetel_persoon
    # def test_get_fractie_zetels_actief(self):
    #     filter = FractieZetel.create_filter()
    #     filter.filter_actief()
    #     zetels = self.api.get_fractie_zetels(max_items=10, filter=filter)
    #     print('fractiezetels:', len(zetels))
    #     for zetel in zetels:
    #         # lid.print_json()
    #         self.assertEqual(zetel.fractie_zetel_persoon.tot_en_met, None)
    #         self.assertEqual(zetel.fractie_zetel_persoon.is_actief, True)


class TestFractieZetelPersoon(TKApiTestCase):

    def test_filter_fractie(self):
        filter = FractieZetelPersoon.create_filter()
        filter.filter_fractie('GroenLinks')
        zetel_personen = self.api.get_items(FractieZetelPersoon, filter=filter)
        self.assertGreaterEqual(len(zetel_personen), 51)

    def test_filter_fractie_actief(self):
        filter = FractieZetelPersoon.create_filter()
        filter.filter_fractie('GroenLinks')
        filter.filter_actief()
        zetel_personen = self.api.get_items(FractieZetelPersoon, filter=filter)
        self.assertGreaterEqual(len(zetel_personen), 14)


class TestFractieZetelVacature(TKApiTestCase):

    def test_get_items(self):
        max_items = 10
        vacatures = self.api.get_items(FractieZetelVacature, max_items=max_items)
        self.assertEqual(max_items, len(vacatures))
        for vac in vacatures:
            print(vac.fractie, vac.functie, vac.van, vac.tot_en_met)
            self.assertIn(vac.functie, FractieZetelVacatureSoort)
            self.assertIsNotNone(vac.fractie)
            self.assertTrue(vac.van)
            self.assertTrue(vac.tot_en_met)
