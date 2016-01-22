## uwaterloo's eValuate export .csv => Dave's .csv file
## by Dave Tompkins

import os.path
import sys

sys.path.append('..')
from csvsimple import *

default_template = '../templates/uw-math-1.csv'

TOKEN_FIELD_SEP = '__TOKEN__FIELD__SEP__'
TOKEN_SEP = '__TOKEN__SEP__'

# This qmap Dict maps Dave's field names to the evaluate question names

qmap_mc = {'mc_1': "Organization",
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
           'mc_15': "Hours Per Week"}

qmap_txt = {'txt_1': "What instructor has done well: ",
            'txt_2': "Improvements to technique or style: ",
            'txt_3': "Course's strong points: ",
            'txt_4': "Course's weak points: ",
            'txt_5': "Class atmosphere: ",
            'txt_6': "Other Comments: "}

hack_map = {"No printed notes": "No printed course notes"}

csv_mc_header = ["mc_1", "mc_2", "mc_3", "mc_4", "mc_5", "mc_6", "mc_7", "mc_8",
                 "mc_9", "mc_10", "mc_11", "mc_12", "mc_13", "mc_14", "mc_15"]

csv_txt_header = ["txt_1", "txt_2", "txt_3", "txt_4", "txt_5", "txt_6"]

def get_response(row, field):
  resp = row[qmap_mc[field]]

  if resp == '':
    return ''

  if resp in hack_map:
    resp = hack_map[resp]

  retval = False

  for x in range(0, 9):
    subfield = field + '.' + str(x)
    if subfield in template and template[subfield].lower() == resp.lower():
      return x

  if not retval:
    print("no match! field [" + field + "] resp = [" + resp + "]")
    exit()


def get_text_response(txt):
  txt = txt.rstrip()
  txt = txt.replace('\n', '[nl]')
  for t in qmap_txt:
    txt = txt.replace(qmap_txt[t], TOKEN_FIELD_SEP + t + TOKEN_SEP)
  txt = txt.replace('[nl]' + TOKEN_FIELD_SEP, TOKEN_FIELD_SEP)
  if txt:
    txt = txt[len(TOKEN_FIELD_SEP):]
    cdict = dict(field.split(TOKEN_SEP) for field in txt.split(TOKEN_FIELD_SEP))
  else:
    cdict = dict()

  for field in csv_txt_header:
    if field not in cdict:
      cdict[field] = ''

  return cdict


# USAGE:
if len(sys.argv) < 3 or len(sys.argv) > 4:
  print("syntax:")
  print("    evaluate-export-csv2csv.py filein.csv fileout.csv [template.csv]")
  exit("missing parameter")
 
file_in = sys.argv[1]
file_out = sys.argv[2]

if len(sys.argv) == 3:
  file_template = default_template
else:
  file_template = sys.argv[3]

if not os.path.isfile(file_in):
  print("error:")
  print("    could not locate required file: " + file_in)
  exit("required file missing")
  
if not os.path.isfile(file_template):
  print("error:")
  print("    could not locate required file: " + file_template)
  exit("required file missing")
  
# warning! this is somewhat fragile
# * no significant format checking
# * assumes question order is fixed

data = SimpleCSV(file_in)
template = csv_to_dict(file_template)

with open(file_out, 'w', encoding='utf-8', newline='') as fout:
  csv_writer = csv.writer(fout)
  csv_writer.writerow(csv_mc_header + csv_txt_header)

  for row in data:
    csv_row = list()
    qcount = 0

    for field in csv_mc_header:
      csv_row.append(get_response(row, field))

    cdict = get_text_response(row['Text Comments'])

    for field in csv_txt_header:
      csv_row.append(cdict[field])

    csv_writer.writerow(csv_row)

