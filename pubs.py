import re
import pandas as pd

''' Generate a tex file. Parse dates from the .bib file
and use pandas for time ordering. Use arXiv number as the data from
which the date is parsed. If not available, use 'year' entry
 of .bib instead.'''

# Parse dates and grab the BibTeX identifiers.
bib = open("biblio.bib", "r")
article = []
arxiv = []
for line in bib:
    if bool(re.findall(r'^@', line)): # BibTeX identifiers.
        article.append(re.findall(r'[a-zA-Z0-9_.-]*:[a-zA-Z0-9_.-]*',
                       line)[0])
        # if no dates are available set date to 2030-01
        arxiv.append('3001')
    if bool(re.findall(r'eprint\s=', line)):# ArXiv identifiers.
        del arxiv[-1]
        if bool(re.findall(r'[0-9]{7}', line)):
            arxiv.append(re.findall(r'[0-9]{7}', line)[0][:4])
        else:
            arxiv.append(re.findall(r'[0-9]{4}\.[0-9]', line)[0][:4])
    elif bool(re.findall(r'year\s=', line)) and arxiv[-1] == '3001':
        print(line, end='')
        del arxiv[-1]
        arxiv.append(re.findall(r'[0-9]{4}', line)[0][2:]+'01')
        print(pd.to_datetime(re.findall(r'[0-9]{4}', line)[0][2:]+'01',
              format = '%y%m'))
bib.close()

# Sort dates with pandas. The year 2030 indicates a record
# with no date and is put at the bottom of the list by setting
# the date to be 1930-01. Needs a bit of work due to ambiguities
# in two-digit years.
pubs = pd.DataFrame()
pubs['arts'] = article
pubs['date'] = arxiv
pubs['date'] = pd.to_datetime(pubs['date'], format = '%y%m')
pubs['date2'] = pubs['date'].apply(lambda x: pd.to_datetime(193001,
    format = '%Y%m') if x.year == 2030 else x)
pubs['date2'] = pubs['date'].apply(lambda x:\
    pd.to_datetime('19'+str(x.year)[2:]+'01',
    format = '%Y%m') if x.year > 2030 else x)
pubs = pubs.sort_values(['date2'], ascending = False)

# Create the LaTeX commands of properly ordered citations.
cites = ''
for name in pubs['arts']:
    cites = cites+"\\nocite{"+name+"}\n"

# Create the tex file
tex_file = open('pubslist.tex', 'w')
tex_string = '\documentclass[a4paper,11pt]{article}\n'\
    '\\usepackage{amsmath,amssymb}\n'\
    '\\bibliographystyle{JHEP.bst}\n'\
    '\\makeatletter\n'\
    '\\renewcommand\@biblabel[1]{\\textbullet}\n'\
    '\\makeatother\n'\
    '\\renewcommand\\refname{List of Publications}\n\n'\
    '\\begin{document}\n'\
    '\\bibliography{biblio.bib}\n'+\
    cites+'\\end{document}'
tex_file.write(tex_string)
tex_file.close()
