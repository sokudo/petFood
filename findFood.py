from typing import List, Optional
import argparse
import json
import sys
import fileinput


def makeArgParser():
  ap = argparse.ArgumentParser(description='Finds pet food by ingredients')
  ap.add_argument(
      '-b',
      '--brands',
      metavar='Brand',
      action="extend",
      nargs="+",
      type=str,
      help='Select brands that match any word in the list.',
      dest='brands'
  )
  ap.add_argument(
      '-bx',
      '--no-brands',
      metavar='Brand',
      action="extend",
      nargs="+",
      type=str,
      help='Exclude brands that match any word in the list.',
      dest='excludedBrands'
  )
  ap.add_argument(
      '-n',
      '--names',
      metavar='Name',
      action="extend",
      nargs="+",
      type=str,
      help='Select foods with names that are matched by any word in the list.',
      dest='names'
  )
  ap.add_argument(
      '-nx',
      '--no-names',
      metavar='Name',
      action="extend",
      nargs="+",
      type=str,
      help='Exclude foods with names that are matched by any word in the list.',
      dest='excludedNames'
  )
  ap.add_argument(
      '-i',
      '--ingredients',
      metavar='Ingredient',
      action="extend",
      nargs="+",
      type=str,
      help='Select only foods where ingredients match ALL words in the list.',
      dest='ingrs'
  )
  ap.add_argument(
      '-ix',
      '--no-ingredients',
      metavar='Ingredient',
      action="extend",
      nargs="+",
      type=str,
      help='Exclude foods where ingredients match ANY word in the list.',
      dest='excludedIngrs'
  )
  ap.add_argument(
      'files',
      metavar='File',
      action="extend",
      nargs="+",
      type=str,
      help='Pet food data file.',
  )

  return ap


def lower(a: Optional[List[str]]) -> Optional[List[str]]:
  return a if not a else [x.lower() for x in a]


def main():
  args = makeArgParser().parse_args()
  args.brands = lower(args.brands)
  args.excludedBrands = lower(args.excludedBrands)
  args.names = lower(args.names)
  args.excludedNames = lower(args.excludedNames)
  args.ingrs = lower(args.ingrs)
  args.excludedIngrs = lower(args.excludedIngrs)

  result = []
  for file in args.files:
    with open(file) as f:
      foods = json.load(f)

    for food in foods:
      lowfood = {
          a: lower(v) if isinstance(v, list) else v.lower() if v else v
          for (a, v) in food.items()
      }
      if match(lowfood, args):
        result.append(food)

  print(json.dumps(result, indent=2))


def match(food, args):
  if args.brands and not any(b in food['brand'] for b in args.brands):
    return False
  if args.excludedBrands and any(b in food['brand']
                                 for b in args.excludedBrands):
    return False

  if args.names and not any(w in food['name'] for w in args.names):
    return False
  if args.excludedNames and any(w in food['name'] for w in args.excludedNames):
    return False

  if args.ingrs:
    if not all(any(i in g for g in food['ingredients']) for i in args.ingrs):
      return False
  if args.excludedIngrs:
    if not all(all(x not in g
                   for g in food['ingredients'])
               for x in args.excludedIngrs):
      return False
  return True


main()