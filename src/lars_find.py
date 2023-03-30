
import re
import sys

from lars_globals import record


# operand-based case-insensitive search (AND, OR, NOT), no regex
def lars_find(records, key, search_attr, case):

   # split key string based on parentheses and spaces
   keys = filter(None, re.split(r'([()]|AND|OR|NOT)', key))
   keys = [k for k in keys if not k.isspace()]

   special_chars = ["AND", "OR", "NOT", ")", "("]

   # this is where the matches go
   found = []

   keywords = []
   statement = ""

   # loop over key terms
   for k in keys:
      if not k in special_chars:
         # loop over lars attributes
         statement_list = []
         for a in search_attr:
            # got new keyword
            keywords.append(k.rstrip().lstrip())
            if case:
               statement_list.append( '''"''' + k.lstrip().rstrip() + '''" in r.''' + a + " ")
            else:
               statement_list.append( '''"''' + k.lstrip().rstrip().lower() + '''" in r.''' + a + ".lower() ")

         sub_statement = "(" + " or ".join(statement_list) + ")"
         statement = statement + sub_statement
            
      else: # connector
         if case:
            statement = statement + " " + k + " "
         else:
            statement = statement + " " + k.lower() + " "

   # THIS IS WHERE THE MAGIC HAPPENS!
   # + some fool-proofery around to save the user from reading tracebacks
   try:
      exec("found = found + [r for r in records if " + statement + "]")
   except SyntaxError:
      print "find: invalid statement"

   if sys.stdout.isatty():
      found = color_matches(found, "|".join(keywords), search_attr)

   return found


# case-insensitive regex search
def lars_find_regex (records, key, search_attr, case):
   
   # here we'll store our matches
   found = []

   # loop over lars attributes
   for a in search_attr:

      # get the job done
      if case:
         found = found + [r for r in records if re.search(key, getattr(r, a)) != None]
      else:
         found = found + [r for r in records if re.search(key.lower(), getattr(r, a).lower()) != None]


   if sys.stdout.isatty():
      found = color_matches(found, key, search_attr)

   return found


# surround matching substrings with color codes for terminal printing
def color_matches (found, kw, search_attr):

   for i, f in enumerate(found):
      for a in search_attr:

         attrstr = getattr(found[i], a)
         key_regex = re.compile(kw, re.IGNORECASE)
         # this is ugly -- I'd be much happier with a re.sub solution if there was one!
         it = key_regex.finditer(attrstr)
         newattrstr = ""
         pos = 0

         for match in it:
            first = match.span()[0]
            second = match.span()[1]
            newattrstr = newattrstr + attrstr[pos:first] + '\033[1;31m' + attrstr[first:second] + '\033[0m'
            pos = second

         newattrstr = newattrstr + attrstr[pos:]
            
         setattr(found[i], a, newattrstr)

   return found

