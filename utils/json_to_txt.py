# Convert JSON sequence of values and write it to a txt file.

import re
import sys
import json

f_in = open('./input.json', 'r', encoding='utf-8')
seq = json.loads(f_in.read())

output = ''
for item in seq:
  output = output + item + '\n'

f_in.close()

f_out = open('output.txt', 'w', encoding='utf-8')
f_out.write(output)
f_out.close()