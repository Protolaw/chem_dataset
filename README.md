Chem dataset
==============================

Parsing and filtering 2d molecules' data

## Prerequisites
**Python 3**

Most of these are okay to install with **pip**. Install the necessary libraries for this project using this command
`pip install -r requirements.txt`

## Getting started

1. **Get the code.**
`$ git clone` the repo and install the Python dependencies
2. **Load the data.**
I don't distribute the data in the Git repo, to get data from Pubchem database by FTP site run the command

```sh
from chem_dataset.data.ftp_download import load_data

load_data()
```

3. **Parse/StandarDize the data.**
In this step (longest by duration) you can choose by which method are going to parse your data (close all your threads for maximum efficiency)

Alternative 1 : by using multiprocessing lib 

```sh
from chem_dataset.data.parser_multi_pool import parse

parse()
```

Alternative 2 : by using Ray framework 
```sh
from chem_dataset.data.parser_ray_pubchem import parse_ray

parse_ray()
```

4. **Remove the duplicates.**
Presence of duplicates can overestimate your results, so to remove them you should run the command

```sh
from chem_dataset.data.dup import delete_dup

delete_dup()
```

You get the standardized and cleaned dataset

5. **Collecting statistics.**
By given parameters collecting statistic from dataset

```sh
from chem_dataset.features.build_features import stat

stat()
```

6. **Visualize the statistics.**
This will visualize the statistics of dataset.
By running following command you have to choose which statistic you have to visualize (by writing in console)
Then user have a choice to [show] the plot, set the boundaries (by command [edit]), [save] the resulting plot or terminate the program execution [exit]

```sh
from chem_dataset.visualization.visualize import vis

vis()
```

Lastly, note that this is currently research code, so a lot of the documentation is inside individual Python files. If you wish to work with this code, you'll have to get familiar with it and be comfortable reading Python code.
