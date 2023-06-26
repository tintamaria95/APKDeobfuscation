import csv
import os

csv_in = open('../javap.csv')
csv_out = open('../javap_processed.csv')

reader = csv.reader(csv_in)

fieldnames = ['class_name', 'meth_name', 'instruction', 'ref']
writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
if os.stat(csv_out).st_size == 0:
    writer.writeheader()

for row in reader:
    if row[3] == '':
        writer.writerow(row)
    # Appelle des instructions / Reconstruction du graphe
    else:
        
