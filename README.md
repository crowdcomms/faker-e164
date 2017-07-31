# Faker Provider for E164 Phone Numbers

`pip install faker-e164`

## Usage

```python
from faker import Faker
from faker_e164.providers import E164Provider
fake = Faker()
fake.add_provider(E164Provider)

# To fake an e164 phone number
fake.e164(region_code="AU", valid=True, possible=True)

# To fake a "safe" e164 phone number from a number of selected regions
fake.safe_e164(region_code="US")
```

## Provider Methods

### e164(*region_code=None*, *valid=True*, *possible=True*) -> *str*

Generate a random phone number for the given `region_code`, if `region_code` is None then a random region will be selected for you.  The *valid* and *possible* arguments toggle validation from the [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) library, the relevant methods are [`is_valid_number` and `is_possible_number`](https://github.com/daviddrysdale/python-phonenumbers#example-usage).

### safe_e164(*region_code=None*) -> *str*

Return a phone number from a list of "safe numbers" as per https://fakenumber.org/.  Supported regions are "AU", "US", "GB", and "CA".

## Contributing

Contributions for faker-e164 are welcomed by the community. If you are looking for issues to work on, please visit [the issues tab](https://github.com/crowdcomms/faker-e164/issues). If you have an idea for an improvement, please submit an new issue and allow some time for discussion before starting any work on a PR. If you get stuck please don't hesitate to start a discussion with the project maintainers.
