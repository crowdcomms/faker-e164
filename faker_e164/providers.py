"""
Provider for faker to generate E164 compatible phone numbers.

`safe_numbers` provided by https://fakenumber.org/australia/mobile
"""
import logging
import phonenumbers
from phonenumbers import PhoneNumber

from faker.providers import BaseProvider
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
    Provider to generate random yet possible phone numbers for various countries
    
    >>> from faker import Faker
    >>> from faker_e164.providers import E164Provider
    >>> fake = Faker()
    >>> fake.add_provider(E164Provider)
    """

    _e164_numerify_pattern = '%###########!!!'

    def _e164_phone_number(self, region_code, is_valid=True, is_possible=True):
        """
        Generate an e164 phone number

        DEPRECATED
        """
        return self._e164(region_code, is_valid=is_valid, is_possible=is_possible)

    def _e164(self, region_code: str, is_valid=True, is_possible=True) -> PhoneNumber:
        """
        Generate an e164 phone number
        """
        phone_number = self.numerify(self._e164_numerify_pattern)
        while not isinstance(phone_number, PhoneNumber):
            try:
                phone_number = phonenumbers.parse(phone_number, region_code)
            except phonenumbers.phonenumberutil.NumberParseException:
                phone_number = self.numerify(self._e164_numerify_pattern)
                continue

            if is_valid and not phonenumbers.is_valid_number(phone_number):
                phone_number = self.numerify(self._e164_numerify_pattern)
                continue

            if is_possible and not phonenumbers.is_possible_number(phone_number):
                phone_number = self.numerify(self._e164_numerify_pattern)
                continue

        return phone_number

    def invalid_e164_phone_number(self, country=None):
        """
        Return an invalid e164 phone number

        DEPRECATED
        """
        logger.warning('invalid_e164_phone_number(...) will be deprecated in favor of the .e164(...) method.')
        countries = ['AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=False,
                                               is_possible=True)
        return phonenumbers.format_number(phone_number,
                                          phonenumbers.PhoneNumberFormat.E164)

    def valid_e164_phone_number(self, country=None):
        """
        Return an invalid e164 phone number.

        DEPRECATED
        """
        logger.warning('valid_e164_phone_number(...) will be deprecated in favor of the .e164(...) method.')
        countries = ['AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=True,
                                               is_possible=True)
        return phonenumbers.format_number(phone_number,
                                          phonenumbers.PhoneNumberFormat.E164)

    def e164(self, region_code: str=None, valid=True, possible=True):
        """Return a random e164 formatted phone number"""
        if region_code is None:
            region_code = self.random_element(phonenumbers.SUPPORTED_REGIONS)
        return self._e164_phone_number(region_code, is_valid=valid, is_possible=possible)

    def safe_e164(self, region_code: str=None):
        """Return a "safe" e164 phone number"""
        return self.random_element(safe_numbers[region_code])
