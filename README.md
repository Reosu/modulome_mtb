# Modular Mycobacterium: Decomposition of Mycobacterium Tuberculosis RNA-Seq Data through Independent Component Analysis

Data repository for applying independent component analysis decomposition on *M. tuberculosis* transcriptomic data, as described in https://www.biorxiv.org/content/10.1101/2021.07.01.450045v1, 

> **Reo Yoo**, Kevin Rychel, Saugat Poudel, Tahani Al-bulushi, Annie Yuan, Siddharth Chauhan, Cameron Lamoureux, Bernhard O. Palsson, and Anand V. Sastry. Machine learning of all Mycobacterium tuberculosis H37Rv RNA-seq data reveals a structured interplay between metabolism, stress response, and infection. _bioRxiv_. 2021.

### Installation

Analysis performed in this data repository require the PyModulon package to be installed. Installation instructions can be found <a href="https://github.com/SBRG/pymodulon">here</a>. 
Once installation is complete install this repository using the following command.
~~~~~~~~~~~~
git clone https://github.com/Reosu/modulome_mtb.git
~~~~~~~~~~~~

Alternatively, one can use a Jupyter server hosted on a Docker container by <a href="https://docs.docker.com/get-docker/">installing Docker</a> and running:
~~~~~~~~~~~~
docker run -p 8888:8888 reosu/modulome_mtb:v1.0
~~~~~~~~~~~~

For additional options, such as mounting local files or changing the the port, see the <a href="https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html">Quick Start Guide</a>.

### Computing iModulon activities for your own data

We have provided a Jupyter notebook that can be used to compute iModulon activities for any new _M. tuberculosis_ transcriptomic dataset in the ``analyze_new_data/`` subfolder. Detailed instructions are listed within this folder.

### iModulonDB Site

iModulonDB is a knowledgebase that allows for easy viewing of iModulon data. A local host of the site containing only *M. tuberculosis* can be run using the following commands:
~~~~~~~~~~~
# Navigate to the iModulonDB folder
cd ../data/iModulonDB

# Run local host
python -m http.server
~~~~~~~~~~~
Once you run the following commands, navigate to localhost:8000 in your browser and enjoy the site! A web version of the site that contains previously published datasets can be found <a href="https://imodulondb.org/">here</a>.

### Repository Structure
+ **Data**: Files created throughout the ICA decomposition and analysis process
  + External
    + Contains files associated with external databases, such as KEGG enrichments, GO enrichments, and metabolic models
  + iModulonDB
    + Contains data files to build the iModulonDB website
  + Interim
    + Data files which have been processed by various pipelines, but require further analysis
    + Includes outputs from ICA decomposition pipeline for multiple dimensionalities
  + Processed Data
    + Contains data that further analyzed and described in the paper
    + Includes X, M, and A matrices, as well as final metadata and TRN files
  + Raw Data
    + Contains transcript counts and multiqc statistic files obtained from SRA data
  + Sequence Files
    + NCBI Sequence files for *M. tuberculosis H37Rv* strain

+ **Notebooks**: Jupyter Notebooks used in the analysis of the data and the creation of figures for the paper
  + *01_expression_QC_SOP* : Takes in the raw counts and multiqc statistics files, filters samples for quality, and produces a log_tpm file
  + *02_expression_visualization* : Visualizes the log_tpm data utilizing a PCA plot and cluster map and normalizes the data to create the log_tpm_norm file
  + *03_ica_dimensionality* : After running ICA decomposition using nextflow, analyzes the outputs at each dimensionality to determine optimal M and A matrices to use
  + *04_iModulon_Data_Obj_Assemble* : Gathers the multiple files and combines them into a complete ica_data object to be used for further analysis
  + *05_QC_QA_Summary* : Notebook that creates summary figures for the QC/QA process and the iModulons
  + *06_Validation_and_Discovery* : Creates figures associated with the validation of the Zur and Lsr2 iModulons, as well as the discovery of new iModulons
  + *07_Core_Lipid* : Creates the venn diagrams used to determine the core lipid response
  + *08_Metabolic_Mapping* : Notebook that utilizes the iEK1008 COBRA model to determine affected pathways during carbon source shifts
  + *09_Oxidative_Stress* : Notebook that creates the figures associated with iModulon response under hypoxia
  + *10_Virulence* : Analysis of iModulons activated during different infection of different host cells
  + *11_Clustering* : Notebook that performs activity clustering utilizing Pearson R and Mutual Information as distance metrics

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

+ **analyze_new_data**: Jupyter Notebook to analyze any new transcriptomic dataset
  + *analyze_new_data*: The jupyter notebook itself
  + README.md: Instructions

+ **mtb_ica.json** : ICA data object used in the analysis described in the paper
+ **License.txt**
+ **environment.yml**
+ **README.md**
