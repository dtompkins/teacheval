## uwaterloo's eValuate raw json => .csv file
## by Dave Tompkins

import csv
import json
import os.path
import sys

# This qmap Dict maps Dave's filed names to the evaluate question names

qmap = {'mc_1': "Organization",
        'mc_2': "Explanations",
        'mc_3': "Questions",
        'mc_4': "Visual Presentation",
        'mc_5': "Oral Presentation",
        'mc_6': "Availability",
        'mc_7': "Interest",
        'mc_8': "Effectiveness",
        'mc_9': "Attendance",
        'mc_10': "Assigned Work",
        'mc_11': "Printed Notes",
        'mc_12': "Textbook",
        'mc_13': "New Material",
        'mc_14': "Assigned Work Amount",
        'mc_15': "Hours Per Week",
        'txt_1': "What instructor has done well",
        'txt_2': "Improvements to technique or style",
        'txt_3': "Course's strong points",
        'txt_4': "Course's weak points",
        'txt_5': "Class atmosphere",
        'txt_6': "Other Comments"}

csv_header = ["mc_1", "mcex_1", "mc_2", "mcex_2", "mc_3", "mcex_3", "mc_4", "mcex_4",
              "mc_5", "mcex_5", "mc_6", "mcex_6", "mc_7", "mcex_7", "mc_8", "mcex_8",
              "mc_9", "mcex_9", "mc_10", "mcex_10", "mc_11", "mcex_11", "mc_12", "mcex_12",
              "mc_13", "mcex_13", "mc_14", "mcex_14", "mc_15", "mcex_15",
              "txt_1", "txt_2", "txt_3", "txt_4", "txt_5", "txt_6"]

def get_response(obj, field):
  resp = ''
  mainkey = 'stats'
  subkey = 'numvalue'
  titlekey = 'title'

  if field.startswith('mcex_'):
    subkey = 'extra'

  if field.startswith('txt_'):
    mainkey = 'text'
    subkey = 'text'

  for q in obj[mainkey]:
    if q[titlekey] == qmap[field.replace('ex', '')]:
      if subkey in q:
        resp = q[subkey]

  if field.startswith('mc_'):
    if resp != '':
      resp = str(int(resp) + 1)

  resp = resp.replace('\r\n', '[nl]')
  resp = resp.replace('[nl][nl]', '[nl]')
  return resp


# USAGE:
if len(sys.argv) != 3:
  print("syntax:")
  print("    evaluate2csv.py filein.json template.csv fileout.csv")
  exit("missing parameter")

file_in = sys.argv[1]
file_out = sys.argv[2]

if not os.path.isfile(file_in):
  print("error:")
  print("    could not locate required file: " + file_in)
  exit("required file missing")

# warning! this is somewhat fragile
# * no significant format checking
# * assumes question order is fixed

with open(file_in, 'r') as f:
  j = json.load(f)

  if not 'objects' in j or len(j['objects']) == 0:
    exit("no responses found")

  with open(file_out, 'w', encoding='utf-8', newline='') as fout:
    csv_writer = csv.writer(fout)
    csv_writer.writerow(csv_header)

    # for each evaluation
    for evaluation in j['objects']:
      csv_row = list()
      qcount = 0

      for field in csv_header:
        csv_row.append(get_response(evaluation,field))

      csv_writer.writerow(csv_row)
