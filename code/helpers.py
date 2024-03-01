import os
import csv

def read_bracket_file(fname):

    bracket = []
    with open(fname) as bracket_file:
        bracket_reader = csv.reader(bracket_file)
        for game in bracket_reader:
            bracket.append(game)
    return(bracket)

def index_csvs_by_year(csv_list):
    data_by_year = {}
    for csv_file in csv_list:
        year = os.path.basename(csv_file).split("_")[0]
        data = read_bracket_file(csv_file)
        data_by_year[year] = data
    return(data_by_year)

def index_by_region(data_by_year):

    regions = ['East', 'Midwest', 'South', 'West']
    data_by_region = {}

    for year in data_by_year:
        data = data_by_year[year]
        data_by_region[year] = {}

        for r in regions:
            data_by_region[year][r] = []

        region_final_matchups = {}

        round_block_start = 0
        for i in 3,2,1,0:
            for r in range(4):
                region = regions[r]
                region_block_size = 2**i
                region_block_start = r * region_block_size

                a = round_block_start + region_block_start 
                b = round_block_start + region_block_start + region_block_size
                data_by_region[year][region] += data[a:b]
                region_final_matchups[region] = data[a:b]
            round_block_start += 2**(i+2)

        # add region champs
        all_champions = set(data[-3] + data[-4])
        for r in data_by_region[year]:
            final = set(data_by_region[year][r][-1])
            data_by_region[year][r].append(list(final.intersection(all_champions)) + [""])

    return(data_by_region)


