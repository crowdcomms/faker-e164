# Faker Provider for E164 Phone Numbers

`pip install faker-e164`

## Usage

```python
from faker import Faker
from faker_e164.providers import E164Provider
fake = Faker()
fake.add_provider(E164Provider)

# To actually fake an e164 phone number
fake.e164()

```

## Contributing

Contributions for faker-e164 are welcomed by the community. If you are looking for issues to work on, please visit [the issues tab](https://github.com/crowdcomms/faker-e164/issues). If you have an idea for an improvement, please submit an new issue and allow some time for discussion before starting any work on a PR. If you get stuck please don't hesitate to start a discussion with the project maintainers.
