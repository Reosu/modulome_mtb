#!/usr/bin/env python3

from glob import glob
import os
import subprocess
from Bio import SeqIO
import pandas as pd
pd.options.mode.chained_assignment = None

#TODO: some genbanks put alternate start codon such as TTG as methionine while others label it as leucine.
#need to check and fix this.

def get_bbh(db1, db2, indir='prots', outdir='bbh', outname=None, mincov=0.8, evalue=0.001, threads=1,
            force=False, savefiles=True):
    """
    Get bidirectional BLAST hits for the two target organisms.
    Parameters
    -----------
    db[1-2]: string
        path to of the 2 targets protein fasta files with a built BLAST db. e.g. '/path/to/file/ecoli.fasta'
    outdir: string, Default 'bbh'
        directory where the outputs will be saved; if dir doesn't exist, it will create one default: bbh
    mincov: float, Default 0.8
        minimum coverage to call hits in BLAST, must be between 0 and 1
    evalue: float, Default 0.001
        evalue threshold for BLAST hits
    threads: int, Default 1
        number of threads to use for BLAST
    force: bool, Default False
        whether to overwrite existing files
    savefiles: bool, Default True
        whether to save the output files to outdir
    outname: string, Default db1_vs_db2_parsed.csv where db[1-2] are the passed arguments
        name of the csv file where that will save the results
    Returns
    -----------
    bbh_res: pandas dataframe containing results and stats from BBH
    """
    #check if files exist, and vars are appropriate
    if not __all_clear(db1, db2, outdir, mincov):
        return None
    #get get the db names, will be used for outfile names
    on1 = '.'.join(os.path.split(db1)[-1].split('.')[:-1])
    on2 = '.'.join(os.path.split(db2)[-1].split('.')[:-1])

    #run and save BLAST results
    bres1 = os.path.join(outdir, '{}_vs_{}.txt'.format(on2, on1))
    bres2 = os.path.join(outdir, '{}_vs_{}.txt'.format(on1, on2))
    
    out1 = __run_blastp(db1, db2, bres1, evalue, threads, force)
    out2 = __run_blastp(db2, db1, bres2, evalue, threads, force)
    
    db1_lengths = __get_gene_lens(db1)
    db2_lengths = __get_gene_lens(db2)
    
    
    if not outname:
        outname = '{}_vs_{}_parsed.csv'.format(on1, on2)
        
    out_file = os.path.join(outdir, outname)
    files=glob(os.path.join(outdir, '*_parsed.csv'))
    
    
    if not force and out_file in files:
        print ('bbh already parsed for', on1, on2)
        out = pd.read_csv(out_file)
        return out
    print('parsing BBHs for', on1, on2)
    
    cols = ['gene', 'subject', 'PID', 'alnLength', 'mismatchCount', 'gapOpenCount', 'queryStart', 
            'queryEnd', 'subjectStart', 'subjectEnd', 'eVal', 'bitScore']
    
    bbh_file1 = os.path.join(outdir,'{}_vs_{}.txt'.format(on1, on2))
    bbh_file2 = os.path.join(outdir,'{}_vs_{}.txt'.format(on2, on1))
    
    bbh = pd.read_csv(bbh_file1, sep='\t', names=cols)
    bbh = pd.merge(bbh, db1_lengths)

    bbh['COV'] = bbh['alnLength']/bbh['gene_length']
    
    bbh2 = pd.read_csv(bbh_file2, sep='\t', names=cols)
    bbh2 = pd.merge(bbh2, db2_lengths) 
    bbh2['COV'] = bbh2['alnLength'] / bbh2['gene_length']
    
    # FILTER GENES THAT HAVE COVERAGE < mincov
    bbh = bbh[bbh.COV >= mincov]
    bbh2 = bbh2[bbh2.COV >= mincov]
    out = pd.DataFrame()
    
    #find if genes are directionally best hits of each other
    for g in bbh.gene.unique():
        res = bbh[bbh.gene == g]
        if len(res) == 0:
            continue
        
        #find BLAST hit with highest percent identity (PID)
        best_hit = res.loc[res.PID.idxmax()]
        res2 = bbh2[bbh2.gene == best_hit.subject]
        if len(res2) == 0: #no match
            continue
        #find BLAST hit with higest PID in the reciprocal BLAST
        best_gene2 = res2.loc[res2.PID.idxmax(), 'subject']
        
        #if doing forward then reciprocal BLAST nets the same gene -> BBH
        if g == best_gene2:
            best_hit['BBH'] = '<=>'
        else: #only best hit in one direction
            best_hit['BBH'] = '->'
        out = pd.concat([out, pd.DataFrame(best_hit).transpose()])
        
    out = out[out['BBH'] == '<=>']
    
    if savefiles:
        print('Saving results to: ' + out_file)
        out.to_csv(out_file)
    else:
        os.remove(bbh_file1)
        os.remove(bbh_file2)
    return out


def __get_gene_lens(file_in):
    """
    Get gene lengths for all the genes in the folder
    Parameters
    -----------
    db: string
        name of the blast database names. e.g. 'ecoli' for blast db generated from ecoli.fa 
    indir: string
        directory containing the blasts db
    Returns
    -----------
    out: pandas dataframe containing the length of each gene in the fasta file
    """
    
    handle = open(file_in)
    records = SeqIO.parse(handle, "fasta")
    out = []
    for record in records:
        out.append({'gene':record.name, 'gene_length':len(record.seq)})
    
    out = pd.DataFrame(out)
    return out


def __run_blastp(db1,db2, out,evalue,threads, force):
    """
    Run protein BLAST
    Parameters
    -----------
    seq: string
        path to file containing the fasta file to BLAST
    db: string
        name of the referece blast database names. e.g. 'ecoli' for blast db generated from ecoli.fa 
    out: string
        file where the BLAST result will be saved
    evalue: float
        evalue threshold for BLAST hits 
    threads: int
        number of threads to use for BLAST
    force: bool, Default False
        whether to overwrite existing files
    Returns
    -----------
    out: pandas dataframe containing the length of each gene in the fasta file
    """
    
    if not force and os.path.isfile(out):
        print(db1, ' already blasted')
        return out
    
    print('blasting {} vs {}'.format(db1, db2))
    cmd_line=['blastp','-db', db1,'-query', db2,'-out', out,'-evalue', str(evalue),'-outfmt', '6',
              '-num_threads', str(threads)]
    
    print('running blastp with following command line...')
    print(' '.join(cmd_line))
    try:
        subprocess.check_call(cmd_line)
    except subprocess.CalledProcessError as err:
        print('BLAST run failed. Make sure BLAST is installed and working properly.')
        raise err
    return out


def __all_clear(db1, db2, outdir, mincov):
    if not 0 < mincov <= 1:
        print('Coverage must be greater than 0 and less than or equal to 1')
        return None
    
    if not (os.path.isfile(db1) and os.path.isfile(db2)):
        print('One of the fasta file is missing')
        return None
    
    for i in ['.phr' , '.pin', '.psq']:
        if not os.path.isfile(db1 + i) or not os.path.isfile(db2 + i):
            print('Some of the BLAST db files are missing')
            return None
        
    if not os.path.isdir(outdir):
        print('Making the output directory: ' + outdir)
        os.mkdir(outdir)
    return True


def __same_output(df1, df2, v=False):
    """
    Function to check if outputs are the same. Used for internal testing only.
    """
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)
    if all(df1.eq(df2)):
        print('The two outputs are the same.')
        return True
    elif all(df1.eq(df2.rename(columns={'subject': 'gene',
                                        'gene': 'subject'}))):
        print('The two outputs are the same, but the genes and subject are switched.')
        return True
    else:
        print('The two outputs are not the same.')
        return False

if __name__== '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Generate bidirectional BLAST hits. Requires BLAST databases for                                                each organism. Output is saved in the \'output\' directory.')
    p.add_argument('db1', help='name of the first BLAST database')
    p.add_argument('db2', help='name of the second BLAST database')
    p.add_argument('-m','--mincov', help='minimum coverage required to call a hit; default 0.8',
                  default=0.8, type=float)
    p.add_argument('-o','--outdir',help='output directory for files. If no directory'
                   'is provided, it will save to \'bbh\' folder', default='bbh')
    p.add_argument('-p', '--threads',  help='number of threads to use for BLAST; default 1', default=1,                          type=int)
    p.add_argument('-e', '--evalue',  help='eval threshold for BLAST hits; default 0.001', type=float,
                  default=0.001)
    p.add_argument('--force', help='Overwrite exisiting BBH files',
                  action='store_true', default=False)
    p.add_argument('--outname', help='Name of the file where the result will be saved')
    params = vars(p.parse_args())
    params.update({'savefiles': True})
#     get_bbh(params['db1'], params['db2'], mincov=params['mincov'],evalue=params['evalue'],
#             force=params['force'], threads=params['threads'], savefiles=True,outname=params['outname'])
    get_bbh(**params)
