import json
import argparse
import csv
import time

parser = argparse.ArgumentParser(description="google cloud transcripts json to csv")
parser.add_argument('-f', '--file', help="json file")

args = parser.parse_args()

if (args.file):
  f = open(args.file)
  data = json.load(f)
  with open(f'{args.file.split(".")[0]}-converted.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['time', 'confidence', 'transcript', 'language'])
    rows = []
    for r in data['results']:
      alternatives = r["alternatives"][0]
      row = []
      if "words" in alternatives:
        startTime = time.strftime("%H:%M:%S", time.gmtime(float(alternatives["words"][0]["startTime"].split('s')[0])))
        endTime = time.strftime("%H:%M:%S", time.gmtime(float(alternatives["words"][-1]["endTime"].split('s')[0])))
        row.append(f'{startTime} - {endTime}')
        print(f'\ntime: {startTime} - {endTime}')
      else:
        row.append('missing')
      if "confidence" in alternatives:
        row.append(f'{alternatives["confidence"]}')
        print(f'confidence: {alternatives["confidence"]}')
      else:
        row.append('missing')
      if "transcript" in alternatives:
        row.append(f'{alternatives["transcript"]}')
        print(f'transcript: {alternatives["transcript"]}')
      else:
        row.append('missing')
      if "languageCode" in r:
        row.append(f'{r["languageCode"]}')
        print(f'language: {r["languageCode"]}')
      else:
        row.append('missing')
      rows.append(row)
    csvwriter.writerows(rows)