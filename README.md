# Pet food data.

Utility to find dog and cat food by ingredients, brands and names. In addition, see calories and urls for each food.

When my dog had an allergy attack, I could not find a food that had no liver besides other requirements.
And I could not find where to look up food just by ingredients, included and excluded.
Here is a result: pet food data in easy to process format and a simple utility to filter them.

Food data is in JSON and contains brand, food name (some as long as a title of a prominent member of the nobility), url to detailed information, calories data and a list of ingredients.

## How to filter

You could filter by brand, food name and ingredients.
You could specify lists of included and excluded things.
Four files with pet food data are provided:

- `dog.dry` has dry dog food data.
- `dog.wet` has wet and canned dog food data.
- `cat.dry` has dry cat food data.
- `cat.wet` has wet and canned cat food data.

To run `findFood.py` you need at least Python 3.8. (Python 3.7 or below would not work).

To view help message:
```
python3 findFood.py -h
```

To select all dry dog food with word instinct in brand name
(such as Nature's Variety Instinct) that do not contain liver:
```
python3 findFood.py dog.dry -b instinct -ix liver
```

To see all cat food by Purina Muse or Purina Beyond that has vitamin A, vitamin E and Taurine but no Carrageenan:
```
/usr/local/opt/python@3.8/bin/python3 findFood.py cat.* -b 'Purina Muse' 'purina bey' -i 'VITAMIN A' 'vitamin E' Taurine -ix Carrageenan > purina.selection
```

Result is output to stdout. It is in the same format as input, and could be used as input data file for `findFood.py`.

## On matching and filtering.

### Matching.

Before matching we change everything into a lower case, to avoid case-related mismatches.
Match is very simple - it succeeds when a brand, name, ingredient or their part (defined on a command line) is a substring of an appropriate field in food data.
E.g. 'instinct' (from -n list) matches 'Instinct Boost Grain Free ...' food name.

### Filtering.

When we filter by brands and food names we select all foods that match any requested brand or food name.

However, with ingredients it's different - we select only those foods that match all requested ingredients.

We exlcude all foods that match any excluded brand, food name or ingredient.
