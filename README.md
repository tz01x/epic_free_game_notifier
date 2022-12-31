# Run in local environment

## Create virtual environment using `conda`
if you do not have conda install in your machine then visit [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for farther instruction 
```
conda create -n env python=3.7
```
## Active virtual environment

```
conda activate env
```

after activated the environment we need to install the dependency

## Install dependency

```
pip install -r requirementes.txt
```
after that we need to migrate 
## Migrate to db
```
pip install migrate
```
## Create a `.env` file to set environment variable
Before running the backend, we need to create a `.env` file at the root directory in this project or you can simply rename `.env.example` file to `.env` file.
Also we need to provide the right credential in environment variable otherwise backend will not run properly 

## Run the backend server

```
pip install runserver --noreload
```


