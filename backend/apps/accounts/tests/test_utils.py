import pytest
from accounts.utils import generate_unique_verification_code


@pytest.mark.django_db
def test_verification_code_length(inactive_account):
    code = generate_unique_verification_code(user=inactive_account)
    assert len(str(code)) == 5


@pytest.mark.django_db
def test_verification_code_unique(inactive_account):
    code = generate_unique_verification_code(user=inactive_account)
    second_code = generate_unique_verification_code(user=inactive_account)
    assert code != second_code
