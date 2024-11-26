#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:33:52 2024

@author: derenbuyuktas
"""
import requests
import csv

# Function to read species names from a file
def read_species_from_file(file_path):
    species_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split line and take the first column
            species = line.split()[0]  # Adjust this if your delimiter is different
            species_list.append(species)
    return species_list

# File path to your input file
file_path = '/Users/derenbuyuktas/Desktop/hhpred_results_OEP/hhpred_results_withoutfiltering_prob70/OEP2/hhpred_OEP2_PDB.txt'  # Adjust the path to your input file

# Read species names from the file
species_list = read_species_from_file(file_path)

# Initialize a list to store phylum results
phylum_list = []

# Loop through each species and fetch phylum information
for species in species_list:
    url = f"https://api.gbif.org/v1/species/match?name={species}"
    response = requests.get(url)

    # Print the response text (optional for debugging)
    # print(f"Response for {species}: {response.text}")

    if response.status_code == 200:
        data = response.json()
        
        # Check if 'phylum' exists in the response
        if 'phylum' in data and data['phylum']:
            phylum_list.append(data['phylum'])  # Append phylum to the list
        else:
            phylum_list.append("Phylum not found")  # Handle missing phylum
    else:
        phylum_list.append("Error fetching data")  # Handle request errors

# Print the final list of phylum
#print(phylum_list)

csv_file_path = '/Users/derenbuyuktas/Desktop/hhpred_results_OEP/hhpred_results_withoutfiltering_prob70/OEP2/phylum_list.csv'  # Adjust path to where you want to save the file

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Species', 'Phylum'])  # Write the header
    for species, phylum in zip(species_list, phylum_list):
        writer.writerow([species, phylum])  # Write species and corresponding phylum

print(f"Phylum data written to {csv_file_path}")