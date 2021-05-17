# Modular Mycobacterium: Decomposition of Mycobacterium Tuberculosis RNA-Seq Data through Independent Component Analysis

Data repository for applying independent component analysis decomposition on *M. tuberculosis* transcritomic data, as described in, 

> **R. Yoo**, AV. Sastry, K. Rychel, BO. Palsson 

### Installation
~~~~~~~~~~~~
git clone https://github.com/Reosu/modulome_mtb.git
~~~~~~~~~~~~

### Repsitory Structure
+ **Data**: Files created througout the ICA decomposition and analysis process
 + External
   + Contains files associated with external databases, such as KEGG enrichments, GO enrichments, and metabolic models
 + iModulonDB
   + Contains data files to build the iModulonDB website
 + Interim
   + Data files which have been processed by various pipelines, but require further analysis
   + Includes outputs from ICA decomposition pipeline for multiple dimesionalities
 + Processed Data
   + Contains data that further analyzed and described in the paper
   + Includes X, M, and A matricies, as well as final metadata and TRN files
 + Raw Data
   + Contains transcript counts and multiqc statistic files obtained from SRA data
 + Sequence Files
   + NCBI Sequence files for *M. tuberculosis H37Rv* strain

+ **Notebooks**: Jupyter Notebooks used in the analysis of the data and the creation of figures for the paper
 + *1_expression_QC_SOP* : Takes in the raw counts and multiqc statistics files, filters samples for quality, and produces a log_tpm file
 + *2_expression_visualization* : Visualizes the log_tpm data utilizing a PCA plot and cluster map and normalizes the data to create the log_tpm_norm file
 + *3_ica_dimensionality* : After running ICA decomposition using nextflow, analyzes the outputs at each dimensionality to determine optimal M and A matricies to use
 + *4_iModulon_Data_Obj_Assemble* : Gathers the multiple files and combines them into a complete ica_data object to be used for futher analysis
 + *5_QC_QA_Summary* : Notebook that creates summary figures for the QC/QA process and the iModulons
 + *6_Validation_and_Discovery* : Creates figures associated with the validation of the Zur and Lsr2 iModulons, as well as the discovery of new iModulons
 + *7_Core_Lipid* : Creates the venn diagrams used to determine the core lipid response
 + *8_Metabolic_Mapping* : Notebook that utilizes the iEK1008 COBRA model to determine affected pathways during carbon source shifts
 + *9_Oxidative_Stress* : Notebook that creates the figures associated with iModulon response under hypoxia
 + *10_Virulence* : Analysis of iModulons activated during different infecton of different host cells
 + *11_Clustering* : Notebook that performs activity clustering utilzing PearsonR and Mutual Information as distance metrics
