import html
import os.path
import pathlib
import shutil
import sys

from csvsimple import *

# CONFIGUARATION SETTINGS:
WWW_OUT_DIR = 'd:/www/teaching/'
DATA_DIR = 'data/'
TEMPLATE_DIR = 'templates/'
CSS_FILE = 'teacheval.css'  # set to '' to not auto copy

NO_COMMENT = 'Coming soon...'

# USAGE:
if len(sys.argv) == 1:
  print("syntax:")
  print("    teacheval.py courseid (do not include the path to data or the .csv)")
  print("or  teacheval.py all")
  exit("missing parameter")


def verify_file(filename):
  """Return filename or gracefully exit if it does not exist"""
  if not os.path.isfile(filename):
    print("error:")
    print("    could not locate required file: " + filename)
    exit("required file missing")
  return filename


def tag_wrap(lst, tag='td', newline='', escape=True):
  """wrap each item in lst with the html tag, e.g.: <tag>first</tag><tag>second</tag>"""
  if escape:
    lst = map(html.escape, lst)
  return '<' + tag + '>' + ('</' + tag + '>' + newline + '<' + tag + '>').join(lst) + '</' + tag + '>'


def sortkey(s):
  """strip out any initial non-alpha chars and convert to lowercase for sorting"""
  return s.lower().lstrip(' -=*!,.:#;@%^&+=_/\\|"\'?()<>[]')

# main program

sections = list()
if sys.argv[1].lower() == 'all':
  for f in pathlib.Path(DATA_DIR).glob('*.csv'):
    if 'responses' not in f.name:
      sections.append(f.name[:-4])
else:
  sections.append(sys.argv[1])

for section_id in sections:
  print("processing " + section_id)

  data = csv_to_dict(verify_file(DATA_DIR + section_id + '.csv'))
  data.update(csv_to_dict(verify_file(TEMPLATE_DIR + data['course'] + '.csv')))

  comment_file = DATA_DIR + section_id + '-comments.txt'
  if os.path.isfile(comment_file):
    with open(comment_file, 'r') as f:
      data['comments'] = f.read()
  else:
    data['comments'] = NO_COMMENT

  with open(verify_file(TEMPLATE_DIR + 'base.html'), 'r') as f:
    base_html = f.read()
  with open(verify_file(TEMPLATE_DIR + data['template'] + '.html'), 'r') as f:
    template_html = f.read()

  qdata = dict()

  if data['template'] != 'comments':

    responses = SimpleCSV(verify_file(DATA_DIR + section_id + '-responses.csv'))

    questions = csv_to_dict(verify_file(TEMPLATE_DIR + data['template'] + '.csv'))
    with open(verify_file(TEMPLATE_DIR + 'mc.html'), 'r') as f:
      mc_html = f.read()
    with open(verify_file(TEMPLATE_DIR + 'txt.html'), 'r') as f:
      txt_html = f.read()

    maxtotal = len(responses)

    for qid in responses.keys:
      if qid[:2] == 'mc' or qid[:3] == 'smc':  # [SUMMARIZED] MULTIPLE CHOICE
        num_choices = 0
        counts = list()
        percents = list()
        choices = list()
        while '{}.{}'.format(qid, num_choices + 1) in questions:
          num_choices += 1
          counts.append(0)
          percents.append('')
          choices.append(questions[qid + '.{}'.format(num_choices)])
        if not num_choices:
          continue
        if qid[:1] == 's':  # sumarized
          assert num_choices == int(responses[0][qid])
          for i in range(0, num_choices):
            counts[i] = int(responses[i + 1][qid])
        else:
          for resp in responses:
            r = resp[qid]
            if r:
              counts[int(r) - 1] += 1
        total = sum(counts)
        maxtotal = max(maxtotal, total)
        if not total:
          continue
        for i in range(0, num_choices):
          if counts[i]:
            percents[i] = str(round(100 * counts[i] / total)) + '%'
            counts[i] = str(counts[i])
          else:
            counts[i] = ''
            percents[i] = ''
        mcdata = {'question_title': html.escape(questions[qid]),
                  'num_choices': num_choices,
                  'td_choices': tag_wrap(choices),
                  'td_counts': tag_wrap(counts),
                  'td_percents': tag_wrap(percents),
                  'css_class': ''}
        if qid + '.css' in questions:
          mcdata['css_class'] = questions[qid + '.css']
        qdata[qid] = mc_html.format_map(mcdata)

      elif qid[:3] == 'txt':  # TEXT RESPONSE
        rlist = list()
        for resp in responses:
          r = resp[qid]
          if r and r.strip():
            rlist.append(r)
        rlist.sort(key=sortkey)

        tdata = {'question_title': html.escape(questions[qid]),
                 'li_responses': tag_wrap(rlist, 'li', '\n').replace('[nl]', '<br />'),
                 'css_class': ''}
        if qid + '.css' in questions:
          tdata['css_class'] = questions[qid + '.css']
        qdata[qid] = txt_html.format_map(tdata)

      else:
        print("could not handle question: " + qid)
        exit("bad question id")

    if 'num-responses' in data:
      maxtotal = int(data['num-responses'])

    if 'num-expected' in data:
      numexp = int(data['num-expected'])
      p = round(100 * maxtotal / numexp)
      qdata['resp_rate'] = "{} / {} ({}%)".format(maxtotal, numexp, p)
    else:
      qdata['resp_rate'] = "{} / ???".format(maxtotal)

  data['body'] = template_html.format_map(qdata)
  page = base_html.format_map(data)

  with open(WWW_OUT_DIR + section_id + '.html', 'w', newline='', encoding='utf-8') as f:
    f.write(page)

if CSS_FILE:
  shutil.copyfile(TEMPLATE_DIR + CSS_FILE, WWW_OUT_DIR + CSS_FILE)
