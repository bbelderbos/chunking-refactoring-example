import os
import re

import pytest

import script


@pytest.fixture(autouse=True)
def delete_previous_run(request):
    def remove_csv_output_files():
        for file in os.listdir("."):
            if re.match(r"sample-\d+\.csv", file):
                os.remove(file)
    request.addfinalizer(remove_csv_output_files)


def test_chunk_csv():
    pass
