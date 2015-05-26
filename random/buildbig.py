import html
import pathlib
import sys

sys.path.append('../')
from csvsimple import *

# CONFIGUARATION SETTINGS:
WWW_OUT_DIR = 'd:/www/teaching/'
WWW_RAND_DIR = WWW_OUT_DIR + 'random/'
BIG_FILE = WWW_RAND_DIR + 'responses.csv'
DATA_DIR = '../data/'
TEMPLATE_DIR = '../templates/'

#todo: if/when uw changes their evaluations, this will become MUCH more complicated.  KISS for now
MATCH_TEMPLATE = 'uw-math-1'
MATCH_TEMPLATE_EX = 'uw-math-1ex'
KEYS = ['mc_1', 'mc_2', 'mc_3', 'mc_4', 'mc_5', 'mc_6', 'mc_7', 'mc_8', 'mc_9', 'mc_10', 'mc_11', 'mc_12', 'mc_13',
        'mc_14', 'mc_15', 'txt_1', 'txt_2', 'txt_3', 'txt_4', 'txt_5', 'txt_6']

OUT_KEYS = KEYS.copy()
OUT_KEYS.extend(['resp_id', 'offering', 'path'])

sections = list()
for f in pathlib.Path(DATA_DIR).glob('*.csv'):
  if 'responses' not in f.name:
    sections.append(f.name[:-4])

total_count = 0
big_list = list()

for section_id in sections:
  print("processing " + section_id)
  data = csv_to_dict(DATA_DIR + section_id + '.csv')
  if data['template'] == MATCH_TEMPLATE or data['template'] == MATCH_TEMPLATE_EX:
    data.update(csv_to_dict(TEMPLATE_DIR + data['course'] + '.csv'))
    offering = data['term'] + ' - ' + data['coursecode'] + ' - ' + data['section']
    path = '../' + section_id + '.html'
    responses = SimpleCSV(DATA_DIR + section_id + '-responses.csv')
    for resp in responses:
      total_count += 1
      rlist = resp.copy()
      resp['resp_id'] = total_count
      resp['offering'] = offering
      resp['path'] = path      
      for k in rlist:
        if k not in KEYS:
          del resp[k]
        if k[:3] == 'txt':
          resp[k] = html.escape(resp[k]).replace('[nl]', '<br />')
      big_list.append(resp)

with open(BIG_FILE, 'w', newline='', encoding='utf-8') as f:
  writer = csv.DictWriter(f, OUT_KEYS)
  writer.writeheader()
  writer.writerows(big_list)

print("DON'T FORGET TO UPDATE total_count in geteval.py")
print("total_count = {}".format(total_count))