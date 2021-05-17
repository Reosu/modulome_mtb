# Modular Mycobacterium: Decomposition of Mycobacterium Tuberculosis RNA-Seq Data through Independent Component Analysis

Data repository for applying independent component analysis decomposition on *M. tuberculosis* transcritomic data, as described in, 

> **R. Yoo**, AV. Sastry, K. Rychel, BO. Palsson 

### Installation

Analysis performed in this data repository require the PyModulon package to be installed. Installation instructions can be found <a href="https://github.com/SBRG/pymodulon">here</a>. 
Once installation is complete install this repository using the following command.
~~~~~~~~~~~~
git clone https://github.com/Reosu/modulome_mtb.git
~~~~~~~~~~~~

### iModulonDB Site

iModulonDB is a knowlegebase that allows for easy viewing of iModulon data. A local host of the site containig only *M. tuberculosis* can be run using the following commands:
~~~~~~~~~~~
# Navigate to the iModulonDB folder
cd ../data/iModulonDB

# Run local host
python -m http.server
~~~~~~~~~~~
Once you run the following commands, navigate to localhost:8000 in your browser and enjoy the site! A web version of the site that contains perviously published datasets can be found <a href="https://imodulondb.org/">here</a>.

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

+ **Supplementary Files** : Supplementary files as listed in the paper
  + *Supplementary_File_1__Dataset_Citations* : List of papers, GEO Datasets, and SRA Datasets used in this study
  + *Supplementary_File_2__TRN_Citations* : List of papers used to create the TRN file
  + *Supplementary_File_3__Lipid_Core* : List of significantly differential iModulons across lipid conditions under various metabolic states
  + *Supplementary_File_4__Carbon_Source_Shift* : List of significantly differential iModulons under different carbon sources at 6 hours and 24 hours
  + *Supplementary_File_5__Hypoxia_Timecourse* : List of significantly differential iModulons during different oxygen levels
  + *Supplementary_File_6__Virulence* : List of significantly differential iModulons during infections of different host cells

+ **Figures**: Contains both interim and complete figures used in the paper
  + Interim: Plots and Charts produced by Jupyter Notebooks which are used to create the final figures
  + Complete: Completed figures as found in the paper

+ **mtb_ica.json** : ICA data object used in the analysis described in the paper
+ **Licence.txt**
+ **enviroment.yml**
+ **README.md**