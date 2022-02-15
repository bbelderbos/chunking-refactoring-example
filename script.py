import csv
import time

startTime = time.time()
chunk_size = 10000

outfile_number = 1
outfile = None

with open('sample.csv', 'r') as infile:
    for index, row in enumerate(csv.reader(infile)):
        if index % chunk_size == 0:
            if outfile is not None:
                outfile.close()
            outfile_name = 'sample-{}.csv'.format(outfile_number)
            outfile = open(outfile_name, 'w')
            outfile_number += 1
            writer = csv.writer(outfile)
        writer.writerow(row)
        executionTime = (time.time() - startTime)

#print('Execution time in seconds: ' + str(executionTime))
data = 'Execution time in seconds: ' + str(executionTime)
print(data)
