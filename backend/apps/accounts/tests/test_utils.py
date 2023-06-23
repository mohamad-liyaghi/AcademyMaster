import pytest
from accounts.utils import generate_unique_verification_code


@pytest.mark.django_db
def test_verification_code_length(deactive_account):
    code = generate_unique_verification_code(account=deactive_account)
    assert len(str(code)) == 5


@pytest.mark.django_db
def test_verification_code_unique(deactive_account):
    code = generate_unique_verification_code(account=deactive_account)
    second_code = generate_unique_verification_code(account=deactive_account)
    assert code != second_code
