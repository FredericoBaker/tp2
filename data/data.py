import pandas as pd
import requests
import shutil
import gzip
import csv
import os

def download_dataset(dataset):

    if os.path.isfile(f'./raw/{dataset}.txt'):
        return

    response = requests.get(f'http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/{dataset}.tsp.gz')

    if not response.ok:
        print(f'Error downloading {dataset}.')
        return

    with open(f'./raw/{dataset}.tsp.gz', mode='wb') as file:
        file.write(response.content)

    with gzip.open(f'./raw/{dataset}.tsp.gz', 'rb') as f_in:
        with open(f'./raw/{dataset}.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(f'./raw/{dataset}.tsp.gz')

def to_csv(dataset):
    with open(f'./raw/{dataset}.txt', 'r') as infile, open(f'./cleaned/{dataset}.csv', 'w', newline='') as outfile:
        reader = infile.readlines()
        writer = csv.writer(outfile)

        writer.writerow(['Node', 'X', 'Y'])

        start_reading = False

        for line in reader:
            if start_reading:
                if line.strip() == 'EOF' or line.strip() == '':
                    break

                parts = line.split()

                # Converte as coordenadas X e Y para inteiros
                node, x, y = parts[0], int(float(parts[1])), int(float(parts[2]))
                writer.writerow([node, x, y])

            elif line.strip() == 'NODE_COORD_SECTION':
                start_reading = True

if __name__ == '__main__':

    df = pd.read_table('tp2_datasets.txt')

    for _, row in df.iterrows():

        dataset = row['Dataset']

        download_dataset(dataset)

        to_csv(dataset)