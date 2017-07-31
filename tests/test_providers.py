"""
Test the E164Provider class
"""
import os
import logging

from typing import Union
from unittest import TestCase, mock

import phonenumbers

from faker import Faker

from faker_e164 import providers
from faker_e164.providers import E164Provider

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
logger = logging.getLogger(__name__)


class E164PhoneNumberProviderTestCase(TestCase):

    provider_class = E164Provider

    def test_e164(self):
        """Test generating e164 phone numbers for all regions"""
        fake = Faker()  # type: Union[E164Provider, Faker]
        fake.add_provider(self.provider_class)
        for region_code in phonenumbers.SUPPORTED_REGIONS:
            phone_number = fake.e164(region_code=region_code)
            self.assertIsInstance(phone_number, str)
            phone_number = phonenumbers.parse(phone_number)
            self.assertTrue(phonenumbers.is_valid_number(phone_number))
        phone_number = fake.e164()
        self.assertIsInstance(phone_number, str)
        phone_number = phonenumbers.parse(phone_number)
        self.assertTrue(phonenumbers.is_valid_number(phone_number))

    def test_e164_is_valid_false(self):
        """Test generating e164 phone numbers for all regions where valid=False"""
        fake = Faker()  # type: Union[E164Provider, Faker]
        fake.add_provider(self.provider_class)
        for region_code in phonenumbers.SUPPORTED_REGIONS:
            phone_number = fake.e164(region_code=region_code, valid=False, possible=True, )
            self.assertIsInstance(phone_number, str)
            phone_number = phonenumbers.parse(phone_number)
            self.assertFalse(phonenumbers.is_valid_number(phone_number))
        phone_number = fake.e164(valid=False, possible=True, )
        self.assertIsInstance(phone_number, str)
        phone_number = phonenumbers.parse(phone_number)
        self.assertFalse(phonenumbers.is_valid_number(phone_number))

    def test_e164_is_possible_false(self):
        """Test generating e164 phone numbers for all regions where valid=False and possible=False"""
        fake = Faker()  # type: Union[E164Provider, Faker]
        fake.add_provider(self.provider_class)
        for region_code in phonenumbers.SUPPORTED_REGIONS:
            phone_number = fake.e164(region_code=region_code, valid=False, possible=False, )
            self.assertIsInstance(phone_number, str)
            phone_number = phonenumbers.parse(phone_number)
            self.assertFalse(phonenumbers.is_possible_number(phone_number))
        phone_number = fake.e164(valid=False, possible=False, )
        self.assertIsInstance(phone_number, str)
        phone_number = phonenumbers.parse(phone_number)
        self.assertFalse(phonenumbers.is_possible_number(phone_number))

    def test_e164_asserts_is_possible_true_if_is_valid_false(self):
        """Regression test that an assertion error is raised for bad `valid` and `possible` arguments"""
        fake = Faker()  # type: Union[E164Provider, Faker]
        fake.add_provider(self.provider_class)
        with self.assertRaises(AssertionError):
            fake.e164(valid=True, possible=False)

    def test_safe_e164(self):
        """Test returning all `safe_numbers`

        Set the `LOGLEVEL` environment variable to 'DEBUG' to see the phone number info for `safe_numbers`"""
        fake = Faker()  # type: Union[E164Provider, Faker]
        fake.add_provider(self.provider_class)

        phone_number = fake.safe_e164()
        self.assertIsInstance(phone_number, str)

        for region_code in providers.safe_numbers.keys():
            with mock.patch('faker_e164.providers.E164Provider.random_element') as random_element:
                random_element.side_effect = providers.safe_numbers[region_code]
                for _ in range(len(providers.safe_numbers[region_code])):
                    phone_number = fake.safe_e164(region_code=region_code)
                    self.assertIsInstance(phone_number, str)
                    if os.environ.get('LOGLEVEL', None) == 'DEBUG':
                        phone_number = phonenumbers.parse(phone_number)
                        logger.debug('Phone Number info: {}\nis_valid: {is_valid}\nis_possible: {is_possible}'.format(
                            phone_number,
                            is_valid=phonenumbers.is_valid_number(phone_number),
                            is_possible=phonenumbers.is_possible_number(phone_number)
                        ))
