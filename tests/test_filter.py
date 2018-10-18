from tkapi.document import ParlementairDocument

from .core import TKApiTestCase


class TestFilters(TKApiTestCase):

    def test_filter_mixin(self):
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_soort('test soort')
        pd_filter.filter_empty_zaak()
        self.assertEqual(len(pd_filter.filters), 2)
