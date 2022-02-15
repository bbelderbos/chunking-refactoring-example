import os
import re

import pytest

import script

CSV_OUTPUT_FILE_PATTERN = re.compile(r"sample-\d+\.csv")


@pytest.fixture(autouse=True)
def delete_previous_run(request):
    def remove_csv_output_files():
        for file in os.listdir("."):
            if CSV_OUTPUT_FILE_PATTERN.match(file):
                os.remove(file)
    request.addfinalizer(remove_csv_output_files)


def test_chunk_csv():
    with open("sample.csv") as f:
        num_chunks = len(f.readlines()) // script.chunk_size + 1
    output_files = [file for file in os.listdir(".")
                    if CSV_OUTPUT_FILE_PATTERN.match(file)]
    assert len(output_files) == num_chunks
