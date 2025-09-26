#!/usr/bin/env python3
import os
import pandas as pd
from xml.etree import ElementTree as ET

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "pmc_oa"))
CSV = os.path.join(DATA_DIR, "PMC_OA_meta.csv")

print('DATA_DIR=', DATA_DIR)
print('CSV=', CSV)

df = pd.read_csv(CSV)
print('Total rows in meta:', len(df))

N = 10
for i in range(min(N, len(df))):
    file_path = df['file_path'].iloc[i]
    pmid = df['PMID'].iloc[i]
    full = os.path.join(DATA_DIR, file_path)
    print('\n--- Row', i, 'PMID=', pmid, 'file_path=', file_path)
    if not os.path.exists(full):
        print(' MISSING:', full)
        continue
    print(' Exists:', full)
    try:
        # read a bit and attempt to parse minimal
        with open(full, 'rb') as f:
            data = f.read(16384)
        text = data.decode('utf-8', errors='replace')
        print(' Snippet (first 400 chars):\n', text[:400])
        # quick parse to count refs and pub-id
        try:
            root = ET.fromstring(text)
            refs = root.findall('.//ref')
            print(' ref count in parsed snippet:', len(refs))
            # search for pub-id elements text
            pubids = root.findall('.//pub-id')
            print(' pub-id count in parsed snippet:', len(pubids))
            for j, pid in enumerate(pubids[:5]):
                attrib = pid.attrib
                print('  pub-id', j, 'attrib=', attrib, 'text=', (pid.text or '')[:80])
        except ET.ParseError:
            print(' Could not parse snippet as XML (truncated snippet). Attempting full parse...')
            try:
                tree = ET.parse(full)
                root = tree.getroot()
                refs = root.findall('.//ref')
                print(' ref count in full parse:', len(refs))
                pubids = root.findall('.//pub-id')
                print(' pub-id count in full parse:', len(pubids))
                for j, pid in enumerate(pubids[:5]):
                    attrib = pid.attrib
                    print('  pub-id', j, 'attrib=', attrib, 'text=', (pid.text or '')[:80])
            except Exception as e:
                print(' Full parse failed:', e)
    except Exception as e:
        print(' Error reading file:', e)

print('\nInspection complete')
