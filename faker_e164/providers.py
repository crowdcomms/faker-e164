"""
Provider for faker to generate E164 compatible phone numbers
"""
import phonenumbers

from faker.providers import BaseProvider


class E164Provider(BaseProvider):
    """
    Provider to generate random yet possible phone numbers for various countries
    
    >>> from faker import Faker
    >>> from faker-e164 import E164Provider
    >>> fake = Faker()
    >>> fake.add_provider(E164Provider)
    """

    def _e164_phone_number(self, country, is_valid=True, is_possible=True):
        """
        Generate an e164 phone number
        """
        phone_number = self.numerify('%###########')
        while not isinstance(phone_number,
                             phonenumbers.phonenumber.PhoneNumber):
            try:
                phone_number = phonenumbers.parse(phone_number, country)
            except phonenumbers.phonenumberutil.NumberParseException:
                phone_number = self.numerify('%###########')
                continue

            if is_valid:
                if not phonenumbers.is_valid_number(phone_number):
                    phone_number = self.numerify('%###########')
                    continue
            if is_possible:
                if not phonenumbers.is_possible_number(phone_number):
                    phone_number = self.numerify('%###########')
                    continue
        return phone_number

    def invalid_e164_phone_number(self, country=None):
        """
        Return an invalid e164 phone number
        """
        countries = ['AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=False,
                                               is_possible=True)
        return phonenumbers.format_number(phone_number,
                                          phonenumbers.PhoneNumberFormat.E164)

    def valid_e164_phone_number(self, country=None):
        """
        Return an invalid e164 phone number
        """
        countries = ['AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=True,
                                               is_possible=True)
        return phonenumbers.format_number(phone_number,
                                          phonenumbers.PhoneNumberFormat.E164)

    def e164(self, region_code=None, phone_number_type=phonenumbers.PhoneNumberType.MOBILE):
        """Return a random e164 formatted phone number"""
        phone_number_obj = phonenumbers.example_number_for_type(region_code, phone_number_type)
        return phonenumbers.format_number(phone_number_obj, phonenumbers.PhoneNumberFormat.E164)