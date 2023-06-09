import pytest
from accounts.utils import generate_unique_verification_code
from core.tests import user


@pytest.mark.django_db
def test_verification_code_length(user):
    code = generate_unique_verification_code(account=user)
    assert len(str(code)) == 5

@pytest.mark.django_db
def test_verification_code_unique(user):
    code = generate_unique_verification_code(account=user)
    second_code = generate_unique_verification_code(account=user)
    assert code != second_code
