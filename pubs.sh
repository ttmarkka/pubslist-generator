# This bash script runs two python scripts and uses pdflatex
# and BibTeX for generating a pdf. Prompts two inputs
# from the user.

# User inputs.
read -p "Inspire author identifier: " bai
read -p "Include unpublished (y/n): " unpubs

# Remove files generated by possible previous passes
rm -f ./files/biblio.bib ./files/pubslist*

# Generate the bibliography
python scraper.py $bai $unpubs

# Generate the tex
python pubs.py

# Generate the pdf. Files are moved around
# for a tidier result.
cp ./files/JHEP.bst JHEP.bst
pdflatex pubslist.tex
bibtex pubslist.aux
pdflatex pubslist.tex
pdflatex pubslist.tex
rm JHEP.bst
mv pubslist* ./files/
mv biblio.bib ./files/

# Automatically open the pdf
# evince ./files/pubslist.pdf
