# Faker Provider for E164 Phone Numbers

`pip install faker-e164`

## Usage

```python
from faker import Faker
from faker_e164.providers import E164Provider
fake = Faker()
fake.add_provider(E164Provider)

# To atually fake an e164 phone number
fake.e164()

```
