import fileinput

for line in fileinput.input():
  print('https://www.chewy.com' + line.strip().split('"')[1])