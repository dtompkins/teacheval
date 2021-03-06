## uwaterloo's eValuate export .csv => Dave's .csv file
## by Dave Tompkins

import os.path
import sys

sys.path.append('..')
from csvsimple import *

# TEMPLATE == '../templates/uw-math-1ex.csv'
num_mc = 15
num_txt = 6

MC_MATCH = 'Question {} Numerical'
MCEX_MATCH = 'Question {} Comment'
TXT_MATCH = 'Text Comments {}'
TXT_Q_MATCH = ["What instructor has done well: ",
               "Improvements to technique or style: ",
               "Course's strong points: ",
               "Course's weak points: ",
               "Class atmosphere: ",
               "Other Comments: "]

csv_mcex_header = list()
for i in range(1, num_mc + 1):
  csv_mcex_header.append("mc_" + str(i))
  csv_mcex_header.append("mcex_" + str(i))

csv_txt_header = list()
for i in range(1, num_txt + 1):
  csv_txt_header.append("txt_" + str(i))


# USAGE:
if len(sys.argv) < 3:
  print("syntax:")
  print("    evaluate-export.py filein.csv fileout.csv")
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

data = SimpleCSV(file_in)

with open(file_out, 'w', encoding='utf-8', newline='') as fout:
  csv_writer = csv.writer(fout)
  csv_writer.writerow(csv_mcex_header + csv_txt_header)

  for row in data:
    csv_row = list()

    for q in range(1, num_mc + 1):
      resp = row[MC_MATCH.format(q - 1)]
      if resp:
        csv_row.append(str((int(resp) + 1)))
      else:
        csv_row.append(resp)
      csv_row.append(row[MCEX_MATCH.format(q - 1)])

    for q in range(1, num_txt + 1):
      txt = ''
      match = TXT_Q_MATCH[q - 1]
      for r in range(0, num_txt):
        resp = row[TXT_MATCH.format(r)]
        if resp and resp[:len(match)] == match:
          txt = resp[len(match):]
      txt = txt.replace('\n', '[nl]')
      csv_row.append(txt)

    csv_writer.writerow(csv_row)
