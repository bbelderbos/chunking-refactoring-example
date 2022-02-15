import csv
from pathlib import Path
import time
import sys

from decorators import timing

startTime = time.time()
chunk_size = 10000


@timing
def chunk_csv(input_file):
    outfile_number = 1
    outfile = None

    input_file_base = Path(input_file).stem
    with open(input_file, 'r') as infile:
        for index, row in enumerate(csv.reader(infile)):
            if index % chunk_size == 0:
                if outfile is not None:
                    outfile.close()
                outfile_name = f"{input_file_base}-{outfile_number}.csv"
                outfile = open(outfile_name, 'w')
                outfile_number += 1
                writer = csv.writer(outfile)
            writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        input_csv = "sample.csv"
    else:
        input_csv = sys.argv[1]
    chunk_csv(input_csv)
