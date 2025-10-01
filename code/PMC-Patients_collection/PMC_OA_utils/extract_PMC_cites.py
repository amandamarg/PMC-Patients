from multiprocessing import Pool, cpu_count
import json
import os
import xml.etree.cElementTree as ET
import pandas as pd
from tqdm import tqdm,trange
from glob import glob
import tarfile
import shutil

# PMC OA directory
data_dir = "../../PMC_OA"

"""
    Extract referece from PMC OA xml.
    Input:
        file_path, PMID
    Output:
        PMID, cites (PMIDs of articles that in this article's reference)
"""
# def extract_cites(msg):
#     file_path, PMID = msg
#     # Some xml files are corrupted.
#     try:
#         # tree = ET.parse(os.path.join(data_dir, file_path))
#         root = tree.getroot()
#     except Exception as e:
#         return PMID, []
#     cites = []
#     for ref in root.iterfind(".//ref"):
#         for id_node in ref.iterfind(".//pub-id"):
#             # Only consider PMID to track citation.
#             if id_node is not None and 'pub-id-type' in id_node.attrib and id_node.attrib['pub-id-type'] == "pmid":
#                 cites.append(id_node.text)
#     return PMID, cites


def getCites(root):
    if root is None:
        return []
    cites = []
    for ref in root.iterfind(".//ref"):
        for id_node in ref.iterfind(".//pub-id"):
            # Only consider PMID to track citation.
            if id_node is not None and 'pub-id-type' in id_node.attrib and id_node.attrib['pub-id-type'] == "pmid":
                cites.append(id_node.text)
    return cites

def extract(group):
    cites = []
    with tarfile.open(group[0]) as t:
        for f in tqdm(group[1]['file_path'].values):
            f_ptr = t.extractfile(f)
            try:
                tree = ET.parse(f_ptr)
                root = tree.getroot()
            except Exception as e:
                root = None
            cites.append(getCites(root))
    return zip(group[1]['PMID'].map(str).values, cites)
                  

if __name__ == "__main__":
    
    # Required on Windows/macOS when using multiprocessing.spawn
    try:
        from multiprocessing import freeze_support
        freeze_support()
    except Exception:
        pass

    # Results from PMC_OA_meta.py
    file_list = pd.read_csv(os.path.join(data_dir, "PMC_OA_meta.csv"))

    data = list(zip(file_list['tar_gz_path'], file_list['file_path'], file_list['PMID']))[:80046]
 
    PMC_cites = {}
 
    groups = [g for g in file_list.groupby("tar_gz_path")]
    
    with Pool(5) as pool:
        PMC_cites.update(dict(pool.map(extract, groups[:50])))

    json.dump(PMC_cites, open(os.path.join(data_dir, "PMC_cites.json"), "w"), indent = 4)
