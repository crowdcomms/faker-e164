"""
Provider for faker to generate E164 compatible phone numbers.

"safe_numbers" provided by https://fakenumber.org/, the GB/United Kingdom "safe_numbers" are reported as invalid by the phonenumbers package.
"""
import os
import logging
import phonenumbers
from phonenumbers import PhoneNumber

from faker.providers import BaseProvider

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

safe_numbers = {
    'AU': [
        '+61491570156',
        '+61491570157',
        '+61491570158',
        '+61491570159',
        '+61491570110',
    ],
    'US': [
        '+12025550191',
        '+12025550188',
        '+12025550187',
        '+12025550137',
        '+12025550105',
        '+12025550124',
    ],
    'GB': [
        '+441632960600',
        '+441632960541',
        '+441632960702',
        '+441632960979',
        '+441632960570',
        '+441632960864',
    ],
    'CA': [
        '+16135550110',
        '+16135550120',
        '+16135550109',
        '+16135550151',
        '+16135550136',
        '+16135550119',
    ]
}


class E164Provider(BaseProvider):
    """
    Provider to generate random phone numbers for various countries
    
    >>> from faker import Faker
    >>> from faker_e164.providers import E164Provider
    >>> fake = Faker()
    >>> fake.add_provider(E164Provider)
    >>> phone_number = fake.e164()
    """

    _e164_numerify_pattern = '%######!!!!!!!!'  # https://en.wikipedia.org/wiki/E.164

    def _get_e164_numerify_pattern(self, region_code: str, is_possible=True):
        if not is_possible:
            return '#!!!!!!'
        country_code = phonenumbers.country_code_for_region(region_code)
        return str(country_code)+self._e164_numerify_pattern[len(str(country_code)):]

    def _e164(self, region_code: str, is_valid=True, is_possible=True) -> PhoneNumber:
        """
        Generate an e164 phone number
        """
        assert not (is_valid and not is_possible), 'is_valid must be False if is_possible is False'
        e164_numerify_pattern = self._get_e164_numerify_pattern(region_code, is_possible=is_possible)
        phone_number = self.numerify(e164_numerify_pattern)
        while not isinstance(phone_number, PhoneNumber):
            try:
                phone_number = phonenumbers.parse(phone_number, region_code)
            except phonenumbers.phonenumberutil.NumberParseException:
                phone_number = self.numerify(e164_numerify_pattern)
                continue

            if is_valid and not phonenumbers.is_valid_number(phone_number):
                phone_number = self.numerify(e164_numerify_pattern)
                continue
            elif not is_valid and phonenumbers.is_valid_number(phone_number):
                phone_number = self.numerify(e164_numerify_pattern)
                continue

            if is_possible and not phonenumbers.is_possible_number(phone_number):
                phone_number = self.numerify(e164_numerify_pattern)
                continue
            elif not is_possible and phonenumbers.is_possible_number(phone_number):
                phone_number = self.numerify(e164_numerify_pattern)
                continue

        return phone_number

    def e164(self, region_code: str = None, valid=True, possible=True) -> str:
        """Return a random e164 formatted phone number"""
        if region_code is None:
            region_code = self.random_element(phonenumbers.SUPPORTED_REGIONS)
        return phonenumbers.format_number(self._e164(region_code, is_valid=valid, is_possible=possible), phonenumbers.PhoneNumberFormat.E164)

    def safe_e164(self, region_code: str = None) -> str:
        """Return a "safe" e164 phone number"""
        if region_code is None:
            region_code = self.random_element(list(safe_numbers.keys()))
        phone_number = phonenumbers.parse(self.random_element(safe_numbers[region_code]))
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

    # Deprecated methods
    def _e164_phone_number(self, region_code, is_valid=True, is_possible=True):  # pragma: no cover
        """
        Generate an e164 phone number

        DEPRECATED
        """
        return self._e164(region_code, is_valid=is_valid, is_possible=is_possible)

    def invalid_e164_phone_number(self, country=None):  # pragma: no cover
        """
        Return an invalid e164 phone number

        DEPRECATED
        """
        logger.warning('invalid_e164_phone_number(...) will be deprecated in favor of the .e164(...) method.')
        countries = ['AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=False, )
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

    def valid_e164_phone_number(self, country=None):  # pragma: no cover
        """
        Return an invalid e164 phone number.

        DEPRECATED
        """
        logger.warning('valid_e164_phone_number(...) will be deprecated in favor of the .e164(...) method.')
        countries = ['AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=True, )
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
