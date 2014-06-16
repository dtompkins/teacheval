# SimpleCSV Class

import csv


class SimpleCSV:
  def __init__(self, filename):
    with open(filename, 'r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      self.filename = filename
      self.keys = reader.fieldnames
      self.data = []
      for row in reader:
        self.data.append(row)
        
  def __len__(self):
    return len(self.data)        

  def __getitem__(self, key):
    return self.data[key]
    
  def __iter__(self):
    for d in self.data:
      yield d

  def save(self, filename=False):
    if not filename: 
      filename = self.filename
    with open(filename, 'w', newline='', encoding='utf-8') as f:
      writer = csv.DictWriter(f, self.keys)
      writer.writeheader()
      writer.writerows(self.data)


def csv_to_dict(filename):
  d = dict()
  with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for key, val in reader:
      d[key] = val
  return d
