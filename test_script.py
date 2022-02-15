from collections import namedtuple
import os
import re

import pytest

from script import chunk_csv, write_chunks, DEFAULT_CHUNK_SIZE

CSV_OUTPUT_FILE_PATTERN = re.compile(r"sample-\d+\.csv")
Content = namedtuple("Content", "num_lines first_line last_line")


@pytest.fixture(autouse=True)
def delete_previous_run(request):
    def remove_csv_output_files():
        for file in os.listdir("."):
            if CSV_OUTPUT_FILE_PATTERN.match(file):
                os.remove(file)
    request.addfinalizer(remove_csv_output_files)


def test_chunk_csv():
    # number of output files
    input_file = "sample.csv"
    chunks = chunk_csv(input_file)
    write_chunks(input_file, chunks)

    with open(input_file) as f:
        num_chunks = len(f.readlines()) // DEFAULT_CHUNK_SIZE + 1
    output_files = [file for file in os.listdir(".")
                    if CSV_OUTPUT_FILE_PATTERN.match(file)]
    assert len(output_files) == num_chunks

    # length and offsets of content
    actual_line_lengths = {}
    for o in sorted(output_files):
        with open(o) as foo:
            lines = foo.readlines()
            content = Content(
                len(lines),
                lines[0].strip(),
                lines[-1].strip())
            actual_line_lengths[o] = content

    expected_content = {
        "sample-1.csv":
        Content(10000, "First Name,Last Name", "John ,Doe 9999"),
        "sample-2.csv":
        Content(10000, "John ,Doe 10000", "John ,Doe 19999"),
        "sample-3.csv":
        Content(10000, "John ,Doe 20000", "John ,Doe 29999"),
        "sample-4.csv":
        Content(10000, "John ,Doe 30000", "John ,Doe 39999"),
        "sample-5.csv":
        Content(10000, "John ,Doe 40000", "John ,Doe 49999"),
        "sample-6.csv":
        Content(10000, "John ,Doe 50000", "John ,Doe 59999"),
        "sample-7.csv":
        Content(2000, "John ,Doe 60000", "John ,Doe 61999"),
    }
    assert actual_line_lengths == expected_content
