# util.py

import re,os
from datetime import date
from modulome.config import *
import urllib.parse
import urllib.request
from io import StringIO

##################################
# Utility fxns for SRA downloads #
##################################

def str2date(date_str):
    ''' Convert date string (YYYY-MM-DD) to a python date object '''
    match = re.search("(\d{4})-(\d\d)-(\d\d)",date_str)
    if match is None:
        raise ValueError('Date must be in YYYY-MM-DD format')
    return date(*[int(x) for x in match.groups()])
    
def get_latest_sra(sra_dir):
    return max([str2date(f) for f in os.listdir(sra_dir) if f.startswith('sra_metadata')])
    
####################################
# Utility fxns for gene annotation #
####################################

def get_attr(attributes,attr_id,ignore=False):
    ''' Helper function for parsing GFF attributes '''
    
    try:
        return re.search(attr_id+'=(.*?)(;|$)',attributes).group(1)
    except:
        if ignore:
            return None
        else:
            raise ValueError('{} not in attributes: {}' \
                             .format(attr_id,attributes))

def gff2pandas(gff_file):
    ''' Converts a GFF3 file to a pandas dataframe '''
    with open(gff_file,'r') as f:
        lines = f.readlines()
    
    # Get lines to skip
    skiprow = sum([line.startswith('#') for line in lines])

    # Read GFF
    names = ['refseq','source','feature','start','end','score','strand',
             'phase','attributes']
    DF_gff = pd.read_csv(gff_file,sep='\t',skiprows=skiprow,
                         names=names,header=None)
    
    # Filter for CDSs
    DF_cds = DF_gff[DF_gff.feature == 'CDS']
    
    # Also filter for genes to get old_locus_tag
    DF_gene = DF_gff[DF_gff.feature == 'gene'].reset_index()
    DF_gene['locus_tag'] = DF_gene.attributes.apply(get_attr,attr_id='locus_tag')
    DF_gene['old_locus_tag'] = DF_gene.attributes.apply(get_attr,
                                                        attr_id='old_locus_tag',
                                                        ignore=True)
    DF_gene = DF_gene[['locus_tag','old_locus_tag']]
                         
    # Sort by start position
    DF_cds = DF_cds.sort_values('start')

    # Extract attribute information
    DF_cds['locus_tag'] = DF_cds.attributes.apply(get_attr,attr_id='locus_tag')
                                                      
    DF_cds['gene_name'] = DF_cds.attributes.apply(get_attr,attr_id='gene',
                                                  ignore=True)
                                                  
    DF_cds['gene_product'] = DF_cds.attributes.apply(get_attr,attr_id='product')
    
    DF_cds['ncbi_protein'] = DF_cds.attributes.apply(get_attr,
                                                     attr_id='protein_id',
                                                     ignore=True)
    
    # Merge in old_locus_tag
    DF_cds = pd.merge(DF_cds,DF_gene,how='left',on='locus_tag',sort=False)
    
    # Check for pseudogenes
    pseudos = DF_cds[DF_cds.locus_tag.duplicated(False)]
    seen = {}
    for i,row in pseudos.iterrows():
        gene = row.locus_tag
        if gene not in seen.keys():
            DF_cds.loc[i,'locus_tag'] = gene+'_1'
            seen[gene] = 1
        else:
            seen[gene] += 1
            DF_cds.loc[i,'locus_tag'] = '{}_{}'.format(gene,seen[gene])

    return DF_cds

##############
# ID Mapping #
##############

def uniprot_id_mapping(prot_list,input_id='ACC+ID',output_id='P_REFSEQ_AC',
                       input_name='input_id',output_name='output_id'):
    ''' Wrapper function for Uniprot Retrieve/ID Mapping '''
    
    url = 'https://www.uniprot.org/uploadlists/'
    
    params = {
    'from': input_id,
    'to': output_id,
    'format': 'tab',
    'query': ' '.join(prot_list)
    }
    
    # Send mapping request to uniprot
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    
    # Load result to pandas dataframe
    text = StringIO(response.decode('utf-8'))
    mapping = pd.read_csv(text,sep='\t',header=0,names=[input_name,output_name])
    
    # Only keep one uniprot ID per gene
    mapping = mapping.sort_values(output_name).drop_duplicates(input_name)
    return mapping

# KEGG conversion tools were adapted from BioPython
    
def kegg_conv(database,query):

    """KEGG conv - convert to KEGG identifiers from NCBI or uniprot identifiers.

    Arguments:
     - database - Target database (ncbi-geneid, ncbi-proteinid, or uniprot)
     - query - input query
    """
    
    if database not in ['ncbi-geneid','ncbi-proteinid','uniprot']:
        raise ValueError('Database must be ncbi-geneid | ncbi-proteinid | uniprot')
    
    url = 'http://rest.kegg.jp/conv/{}/{}'.format(database,query)

    # Send mapping request to kegg
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as f:
        response = f.read()

    # Load result to pandas dataframe
    text = StringIO(response.decode('utf-8'))
    mapping = pd.read_csv(text,sep='\t',header=None,names=['kegg_id',database])
    mapping[database] = [entry[entry.find(':')+1:] for entry in mapping[database]]
    return mapping
