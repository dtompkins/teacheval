#!/usr/bin/python3

import csv
import json
import random

print("Content-type: application/json")
print()

#todo: make this more robust.  currently I only have to change it once a term
total_count = 1930
random.seed()
resp_id = random.randrange(total_count) + 1

#todo: currently, just reading in all of the file is "fast enough"
with open('responses.csv', 'r') as f:
  responses = csv.DictReader(f)
  count = 0
  for r in responses:
    count += 1
    if count == resp_id:
      print(json.dumps(r))
      break
