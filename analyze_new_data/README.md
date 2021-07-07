# Computing iModulon activities for new datasets

The iModulon structure of *M. tuberculosis* can be used to easily analyze new datasets (See [Sastry et al. 2021](https://www.biorxiv.org/content/10.1101/2021.07.01.450581v1)). This method does not re-compute the iModulons. Instead, it uses a pre-computed iModulon structure to infer the activities of new RNA-seq datasets. Due to this caveat, it can only find activities for iModulons defined in this study (See [here](https://imodulondb.org/dataset.html?organism=m_tuberculosis&dataset=modulome) for a complete list). If your experiment activates new transcriptional regulators not listed here, we cannot detect this without re-running ICA, which is a computationally intensive process.

For most purposes, the iModulon activities computed here will be accurate, since this structure is built using over 650 expression profiles.

## Instructions
1. Install [Docker](https://docs.docker.com/get-docker/)
2. Compute Transcripts per Million (TPM) for your expression profiles. This file should look like `example_data.csv`.
3. Add your TPM file to this folder.
4. Start the Jupyter server by running the following command in Terminal:
```bash
docker run -p 8888:8888 -v "${PWD}":/home/jovyan/work reosu/modulome_mtb:v1.0
```
    * -p: Sets the port to 8888
    * -v: Mounts the local directory to `/home/jovyan/work` in the Docker container
5. Open the link in Terminal that begins with `127.0.0.1` and navigate to the `work` folder
6. Open the `analyze_new_data.ipynb` notebook and follow the instructions in the notebook

## Mathematical Background

ICA computes two matrices from the e**X**pression matrix: the i**M**odulon matrix, which contains the iModulon structure, and the **A**ctivity matrix, which contains the iModulon activities. These matrices are related through the following equation:

$ \mathbf{X}=\mathbf{M}\cdot \mathbf{A} $

We can therefore infer iModulon activities for a new expression dataset **X'** as follows:

$ \mathbf{A'}=\mathbf{M^{-1}}\cdot \mathbf{X'} $

This is implemented in the *infer_imodulon_activities* function in the [PyModulon](https://pymodulon.readthedocs.io/en/latest/) package
