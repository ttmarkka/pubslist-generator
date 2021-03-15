import requests as req
import sys
import re


''' Using requests for accessing the INSPIRE REST API.'''

# Two inputs from user for the search.
bai = sys.argv[1]
if sys.argv[2] == 'n':
    doc_type = '&doc_type=published'
else:
    doc_type = ''

#Perform the request. Cut-off at 1000 items.
query = '?q=f+a+{}+{}&size=1000'.format(bai, doc_type)
url = 'https://inspirehep.net/api/literature/'
resp = req.get(url+query)
download_url = resp.json()['links']['bibtex']
response = req.get(download_url)

# Save the bibliography.
with open('biblio.bib', 'w') as bib_file:
    bib_file.write(response.text)
