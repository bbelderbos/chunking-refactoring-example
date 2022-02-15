import os
import re

import pytest

import script


@pytest.fixture(autouse=True)
def delete_previous_run():
    for file in os.listdir("."):
        if re.match(r"sample-\d+\.csv", file):
            print("remove file", file)
            os.remove(file)


def test_chunk_csv():
    pass
