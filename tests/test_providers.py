"""
Test the E164Provider class
"""
from unittest import mock, TestCase

from faker_e164.providers import E164Provider


class E164PhoneNumberProviderTestCase(TestCase):

    def test_valid_e164_phone_number(self):
        provider = E164Provider(None)
        phone_number = provider.valid_e164_phone_number()

        with mock.patch('faker.providers.BaseProvider.numerify') as numerify:
            def g():
                yield 'badnumber'
                yield '+61426814275'
            numerify.side_effect = iter(g())
            provider.valid_e164_phone_number()

    def test_invalid_e164_phone_number(self):
        provider = E164Provider(None)
        phone_number = provider.invalid_e164_phone_number()
