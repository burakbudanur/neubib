import bibtexparser as bp
import re
    
with open("neu.bib") as bibfile:
    bib_db = bp.bparser.BibTexParser(common_strings=True).parse_file(bibfile)

db = bp.bibdatabase.BibDatabase()
ids = []

for entry in bib_db.entries:

    hentry = bp.customization.homogenize_latex_encoding(entry)
 
    try: 
        authors = hentry['author']
    except: 
        try: 
            authors = hentry['editor']
        except:
            print(f"Warning: no author or editor found in entry {hentry['ID']} ... "
                  f"this entry will be discarded from the formatted bib file... ")
        
            continue

    first_author = []

    for string in authors.split():

        if string.lower() == 'and':
            break
        
        first_author.append(string)
    
    name = ""

    initial_dot = False
    for i, string in enumerate(first_author):
        if '.' in string:
            initial_dot = True
            continue
        elif initial_dot:
            name += string
        elif ',' in string:
            # Lastname, F.
            for j in range(0, i + 1):
                name += first_author[j]
            break
        elif 'jr' in string.lower():
            for j in range(0, i + 1):
                name += first_author[j]
            break

    if name == "":
        name = first_author[-1]    


    name = re.sub(r'\W+', '', name)
    try:
        year = hentry['year']
    except:
        year = 'noyear'
    
    try: 
        ltitle = hentry['title'].split()
        title = re.sub(r'\W+', '', ltitle[0])
        if title.lower() in ('the', 'a', 'an'):
            title = re.sub(r'\W+', '', ltitle[1])
    except:
        title = 'notitle'
    
    new_id = (name+year+title).lower()

    if new_id not in ids:
        hentry['ID'] = new_id
        ids.append(new_id)
    elif new_id+'b' not in ids:
        hentry['ID'] = new_id+'b'
        ids.append(new_id+'b')
    elif new_id+'c' not in ids:
        hentry['ID'] = new_id+'c'
        ids.append(new_id+'c')
    elif new_id+'d' not in ids:
        hentry['ID'] = new_id+'d'
        ids.append(new_id+'d')
    
    # add the formatted entry to the db
    db.entries.append(hentry)

with open('neu.bib', 'w') as bibtex_file:
    bp.dump(db, bibtex_file)
            

    #db.entries.append(hentry_formatted)
