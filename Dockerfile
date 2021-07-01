# Make sure to start with a .dockerignore file that contains at least .git (see file in this repo)
# To build the docker container, run
#
#       docker build . -t <username>/<repo_name>:<version>
#
# Once you've tested the container and are ready to publish, run
#
#       docker push <username>/<repo_name>:<version>
#


# Start with PyModulon base container
FROM sbrg/pymodulon:v0.2.1

# Add your contact information
LABEL maintainer="Anand Sastry <avsastry@eng.ucsd.edu>"

# Change to root user for installation
USER root

# Install R
RUN apt-get update --yes && \
    # Install R dependencies
    apt-get install --yes --no-install-recommends \
    gfortran \
    liblapack-dev \
    libopenblas-dev && \
    # Clean up
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python/R libraries
RUN conda install --quiet --yes -c conda-forge -c bioconda \
    'r-base=4.1.0' \
    'r-irkernel=1.2*' \
    'r-treemap=2.4*' \
    'rpy2=3.4*' \
    'escher=1.7*' \
    'cobra=0.21*' && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Change user back to NB_USER
USER $NB_USER

# Install python venn package
RUN pip install venn==0.1.3

# Copy the repository to the container. Make sure your .dockerignore file skips any unnecessarily large files
COPY --chown=$NB_USER:$NB_GID . /home/${NB_USER}/modulome_mtb

# Make sure to test your container and ensure that everything runs!
