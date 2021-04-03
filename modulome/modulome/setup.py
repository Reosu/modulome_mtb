from setuptools import setup,find_packages
setup(name="modulome",
      version="0.1",
      author="Anand Sastry",
      author_email="avsastry@eng.ucsd.edu",
      description="Scripts and variables for the modulome pipeline",
      packages=find_packages(),
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
      python_requires='>=3.6')
