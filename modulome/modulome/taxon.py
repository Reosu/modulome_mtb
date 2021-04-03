# taxon.py

from Bio import Entrez

def format_name(name):
    genus = name.split()[0]
    rest = name.split()[1:]
    return genus[0]+'. '+' '.join(rest)
    
def get_tax_dict(id_list,reformat=True):
    handle = Entrez.efetch(db='taxonomy',id=[str(x) for x in id_list])
    record = Entrez.read(handle)
    if reformat:
        tax_dict = {int(rec['TaxId']):format_name(rec['ScientificName']) for rec in record}
    else:
        tax_dict = {int(rec['TaxId']):rec['ScientificName'] for rec in record}
    tax_dict['Other'] = ''
    return tax_dict
    
def get_tax_name_counts(counts,reformat=True,threshold=0):
    id_list = counts[counts>threshold].index
    id_list = [x for x in id_list if x != 'Other']
    if id_list == []:
        return []
    else:
        tax_dict = get_tax_dict(id_list,reformat)
        return [tax_dict[tax_id] if tax_id in tax_dict.keys() else '' for tax_id in counts.index]
    
def get_strain(tax_id,tax_rank_dict,parent_tax_dict):
    old_id = -1
    new_id = tax_id
    id_branch = [tax_id]
    while tax_rank_dict[new_id] not in ['species','superkingdom']:
        old_id = new_id
        new_id = parent_tax_dict[old_id]
        id_branch.append(tax_id)
        
    if new_id == 2: # Bacteria
        return -1
    elif len(id_branch) >= 3:
        return id_branch[-3]
    elif len(id_branch) >= 2:
        return id_branch[-2]
    else:
        return id_branch[-1]
        
def get_species(tax_id,tax_rank_dict,parent_tax_dict):
    old_id = -1
    new_id = tax_id
    while tax_rank_dict[new_id] not in ['species','superkingdom']:
        old_id = new_id
        new_id = parent_tax_dict[old_id]    
    if new_id == 2: # Bacteria
        return -1
    else:
        return new_id 

def get_class(tax_id,tax_rank_dict,parent_tax_dict):
    old_id = -1
    new_id = tax_id
    while tax_rank_dict[new_id] not in ['class','superkingdom']:
        old_id = new_id
        new_id = parent_tax_dict[old_id]
    if new_id == 2: # Bacteria
        return -1
    else:
        return new_id
