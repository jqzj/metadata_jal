#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import re
import csv
import sys
import os

# this function retrieves ICPSR DOIs that are currently in DataCite
def get_dois_in_datacite(prefix, base_url, header, authorization):
    icpsr_dois_in_datacite = []
    page = 1

    while True:
        url = f"{base_url}?query=prefix:{prefix}&page[size]=100&page[number]={page}"

        response = requests.get(url, headers=header, auth=authorization)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' not in data or len(data['data']) == 0:
                break

            for item in data['data']:
                id = item['id'].lower()
                # Extract the five-digit study number and check if it matches the expected ICPSR format
                match = re.match(rf"^{prefix}/icpsr\d{{5}}$", id)
                if match:
                    icpsr_dois_in_datacite.append(id)

            # Check if there are more pages
            if 'links' in data and 'next' in data['links']:
                page += 1
            else:
                break

        else:
            print(f"Error retrieving DOIs: {response.status_code} {response.text}")
            break

    return icpsr_dois_in_datacite


# Function to retrieve existing related items
def get_existing_related_items(doi, url, header, authorization):

    response = requests.get(url, headers=header, auth=authorization)
    if response.status_code == 200:
        data = response.json()
        return data['data']['attributes'].get('relatedIdentifiers', [])
    elif response.status_code == 404:
        print(f"DOI not found: {doi}")
        return None
    else:
        print(f"Error retrieving related items for DOI {doi}: {response.status_code} {response.text}")
        return None

def main():

    # set variables
    input_file = 'C:/icpsr_github/metadata/datacite/bib-dois-0724.xlsx'
    output_file = 'C:/icpsr_github/metadata/datacite/updated_dois.csv'
    search_prefix = "10.81037"
    label_mapping = {
        'JOUR': 'JournalArticle',
        'CHAP': 'BookChapter',
        'NEWS': 'Text',  
        'MGZN': 'JournalArticle',
        'ADVS': 'Audiovisual',
        'GEN': 'Text',              
        'CONF': 'ConferencePaper',
        'BOOK': 'Book',
        'RPRT': 'Report',
        'THES': 'Dissertation',
        'ELEC': 'Other',
        'MANSCPT': 'Preprint'
    }

    #make sure our input file actually exists
    if not os.path.exists(input_file):
        print(f"{input_file} does not exist; check path and run script again")
        sys.exit(1)

    # load the spreadsheet
    df = pd.read_excel(input_file)

    # loop through our data and make a dict of all our studies that have citations
    print('\nGetting info from DBInfo spreadsheet')
    icpsr_doi_dict = {}
    for index, row in df.iterrows():
        
        #skip any rows with no study numbers 
        if not row['STUD_NUMS']:
            continue

        #split up study numbers; strip any white space and pad to 5 digits
        for study_num in str(row['STUD_NUMS']).split(';'):
            study_num = study_num.strip()
            if len(study_num) == 4:
                study_num = '0' + study_num
            full_doi = f"{search_prefix}/icpsr{study_num}"

            # check to see if our dict already has this DOI; if not, add it, with an empty list as the value
            if not icpsr_doi_dict.get(full_doi):
                icpsr_doi_dict[full_doi] = []
            
            # add the related pub info to a temporary dict; then append to the DOI list
            rel_pub_info = {
                    "relationType": "IsCitedBy",
                    "relatedIdentifier": row['DOI'].strip(),
                    "relatedIdentifierType": "DOI",
                    "resourceTypeGeneral": label_mapping.get(row['RIS_TYPE'].strip(), 'Other')
                }
            icpsr_doi_dict[full_doi].append(rel_pub_info)

    # Now that we have all of our local citations in a dict, we will see what citataions datacite knows about
    # Declare DataCite API variables 
    base_url = "https://api.test.datacite.org/dois" 
    username = "ICPSR.PFKTGI"
    api_key = "88Yzq-tVgJE-SGMG2-zXNBs-kW9dc-dqzML-eEFBL"
    authorization = HTTPBasicAuth(username, api_key)
    header = {
        "content-type": "application/json",
        "authorization": f"Basic {username}:{api_key}"
    }

    #first, we'll see all the DOIs registered by Datacite
    print('\nSeeing which items have DOIs in DataCite...')
    icpsr_dois_in_datacite = get_dois_in_datacite(search_prefix, base_url, header, authorization)

    #loop through our local dict; retrieve record from DataCite and compare citations
    updated_dois = {}
    running_count = 0
    for icpsr_doi, current_icpsr_pubs in icpsr_doi_dict.items():

        #skip item if it doesn't actually have a datacite DOI
        if icpsr_doi not in icpsr_dois_in_datacite:
            continue
        
        print(f'\nWorking on {icpsr_doi}\n')

        # create the URL for our API call; then use it to get any relatedIdentifiers currently in DataCite
        url = f"{base_url}/{icpsr_doi}"
        current_datacite_relatedIdentifiers = get_existing_related_items(icpsr_doi, url, header, authorization)

        # NOTE: if the function returns None (no DataCite record found) just continue.  
        if current_datacite_relatedIdentifiers is None:
            continue 

        # if we did retrieve related Identifiers, we need to check to see if they include any of our Bibliography entries. First, get all the related pub DOIs we found in datacite
        dc_pub_dois = {pub['relatedIdentifier'] for pub in current_datacite_relatedIdentifiers}

        # Next, ID all the ICPSR bibliography entries that are already in datacite
        duplicate_pubs = [p for p in current_icpsr_pubs if p['relatedIdentifier'] in dc_pub_dois]

        # if any duplicate items were found, remove from our list
        if duplicate_pubs:
            for item in duplicate_pubs:
                current_icpsr_pubs.remove(item)

        # Finally, combine our two lists so that we don't lose any info
        all_related_pubs = current_icpsr_pubs + current_datacite_relatedIdentifiers

        # if we don't have any new info to write, skip to the next study
        if all_related_pubs == current_datacite_relatedIdentifiers:
            print('\tNo new pubs to add; moving on to next item...\n')
            continue

        #track how many pubs we will be adding
        updated_pubs = len(all_related_pubs) - len(current_datacite_relatedIdentifiers)
        running_count += updated_pubs
        print(f'\t{updated_pubs} publications to update.') 

        # Now we are ready to write to DataCite; set up our payload and then use an HTTP PUT call
        payload = {
            "data": {
                "type": "dois",
                "attributes": {
                    "relatedIdentifiers": all_related_pubs
                }
            }
        }
        
        response = requests.put(url, json=payload, headers=header, auth=authorization)
        
        # # document the status of request; '200' code is success
        if response.status_code == 200:
            print(f"\tSuccessfully updated DOI {icpsr_doi}")

            # note statistics in our tracking dict
            updated_dois[icpsr_doi] = {
                "current": len(current_datacite_relatedIdentifiers),
                "updated": updated_pubs,
                "total": len(all_related_pubs)
            }
        else:
            print(f"\tFailed to update DOI {icpsr_doi}: {response.status_code} {response.text}") 

    print(f"\n\nTotal DOIs updated: {len(updated_dois)}")
    print(f"Total pubs added: {running_count}")

    # Write updated DOIs to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        #Write header row
        writer.writerow(['DOI', '# of Existing DataCite Pubs', '# of Newly-Added Pubs', 'Total # of Pubs'])  # 
        
        #Loop through our dictionary and write info for each DOI
        for doi, num in updated_dois.items():
            writer.writerow([doi, num['current'], num['updated'], num['total']])  # Write each DOI and the # of updated pubs

if __name__ == "__main__":
    main()




