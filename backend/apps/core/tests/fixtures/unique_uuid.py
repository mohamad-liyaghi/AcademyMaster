import pytest
import uuid
import time


@pytest.fixture
def unique_uuid():
    '''Generate a unique uuid based on the time'''
    time_based_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))
    return time_based_uuid
