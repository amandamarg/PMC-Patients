import os
import pandas as pd
import re
import json
from tqdm import trange, tqdm


# PMC_OA dataset downloaded from https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/
data_dir = "../../PMC_OA"

# PMID/PMCID converter downloaded from https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/
ID_converter = pd.read_csv(os.path.join(data_dir, "PMC-ids.csv"))
ID_dict = {}
for i in trange(len(ID_converter)):
    PMC_id = ID_converter['PMCID'].iloc[i]
    PMID = str(ID_converter['PMID'].iloc[i])
    # Filter those without PMID
    if PMID != '0' and PMID != 'nan' and PMID != '':
        ID_dict[PMC_id] = PMID.replace('.0', '')

subsets = ["comm", "noncomm", "other"]

file_paths = []
PMIDs = []
PMID_set = set()
Licenses = []
tar_gz_paths = []
for subset in subsets:
    directory = os.path.join(data_dir, subset, 'xml')
    csvs = filter(lambda x: x.endswith(".csv"), os.listdir(directory))
    
    for csv in tqdm(list(csvs)):
        tar_gz_path = os.path.join(directory, csv.replace("filelist.csv", "tar.gz"))
        try:
            filelist = pd.read_csv(os.path.join(directory, csv))
            for i in range(len(filelist)):
                file_path = filelist['Article File'].iloc[i]
                PMID = str(filelist['PMID'].iloc[i])
                License = filelist['License'].iloc[i]
                if not PMID:
                    PMID = '0'

                PMC_id = file_path[(file_path.find("/PMC") + 1) : -4]
                if PMC_id in ID_dict.keys():
                    if ID_dict[PMC_id] != PMID:
                        PMID = ID_dict[PMC_id]
                
                if (PMID == '0') or (PMID in PMID_set):
                    continue
                
                tar_gz_paths.append(tar_gz_path)
                # file_paths.append(directory.split('/')[-1] + '/' + file_path)
                file_paths.append(file_path)
                PMIDs.append(PMID)
                PMID_set.add(PMID)
                Licenses.append(License)
        except:
            print(os.path.join(directory, csv))
            continue

try:
    data = pd.DataFrame({"tar_gz_path": tar_gz_paths, "file_path": file_paths, "PMID": PMIDs, "License": Licenses})
    data.to_csv(os.path.join(data_dir, "PMC_OA_meta.csv"))
except Exception as e:
    print(e)
    import ipdb; ipdb.set_trace()
