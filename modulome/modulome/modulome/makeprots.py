#!/usr/bin/env python

from Bio import SeqIO

def makeprots(gbk, out):
    """
    Makes protein files for all the genes in the genbank file
    Parameters
    ----------
    gbk: string
        path to the input genbank file
    out: string
        path to the outfut fasta file
    """
    with open(out, 'w') as fa:
        for refseq in SeqIO.parse(gbk, 'genbank'):
            for feats in [f for f in refseq.features if f.type == 'CDS']:
                lt = feats.qualifiers['locus_tag'][0]
                try:
                    seq = feats.qualifiers['translation'][0]
                except KeyError:
                    seq = feats.extract(refseq.seq).translate()
                if seq:
                    fa.write('>{}\n{}\n'.format(lt, seq))
                    
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Generate protein fasta file from genbank files.')
    p.add_argument('gbk', help='Paths to genbank file.', type=str)
    p.add_argument('out', help='Path to fasta file where the protein seqs will be written.', type=str)
    params = vars(p.parse_args())
    makeprots(**params)