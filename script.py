from collections import defaultdict
import csv
from pathlib import Path
import time
import sys

from decorators import timing

startTime = time.time()
chunk_size = 10000


@timing
def chunk_csv(input_file):
    files = defaultdict(list)

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        rows = []
        for index, row in enumerate(reader):
            if index % chunk_size == 0 and index > 0:
                yield rows
                rows = []
            rows.append(row)
        yield rows

@timing
def write_chunks(input_file, chunks):
    input_file_base = Path(input_file).stem

    for index, rows in enumerate(chunks, start=1):
        outfile = f"{input_file_base}-{index}.csv"
        with open(outfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        input_file = "sample.csv"
    else:
        input_file = sys.argv[1]
    chunks = chunk_csv(input_file)
    write_chunks(input_file, chunks)
