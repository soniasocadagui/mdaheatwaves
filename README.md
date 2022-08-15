# mdaheatwaves
<img src="https://github.com/soniasocadagui/mdaheatwaves/blob/main/img/Kuleuven.png" width="100"/>

# Heat Wave Impacts on Human Health
## Description

The immediate effects of high temperatures on physical human health are pretty evident and well-known. However, the knowledge about possible long-term impacts of extreme heat on mental health is still in research, as well as the study of the deterioration of chronic diseases due to exposure to harsh hot weather. In addition, as the expectation is that climate change will raise the global average temperature in the coming years, also heat waves will get even worse. Therefore, addressing the potential impact of soaring temperatures on mental and chronic health conditions is essential to create public health measures to tackle these issues properly in the forthcoming times.

## Directory explanation

```
Heat Waves Impacts
├── code: Contains the Jupyter notebooks used
│   ├── 1.Processing_Data.ipynb
│   ├── 2.Clustering.ipynb
│   ├── 3.Modeling.ipynb
│   └── my_functions.py
├── data: Contains the datasets downloaded to develop the project
│   ├── country codes
│   ├── Global Burden of Disease study: This dataset is available in the drive folder because of its size.  
│   ├── population
│   ├── Suicide rate estimates, crude
│   ├── Temperature data: This dataset is available in the drive folder because of its size.
│   └── features_diccionary.csv
├── img: Contains the KU Leuven logo
├── models: Contains the models created to predict suicide rate
│   ├── best_params_RandomForest.pkl
│   ├── best_params_XGboost.pkl
│   ├── elasticnet_model.pkl
│   ├── RandomForest_model.pkl
│   └── XGboost_model.pkl
└── output: Contains the processed data, and the results obtained from the clustering analysis 
└── requirements.txt: Contains all the packages used in the project

```

## Instructions to run this repository's code

1. Clone the repository.
```
git clone -b main https://github.com/soniasocadagui/mdaheatwaves.git
```
2. Create a new virtual environment with Python 3.9.5 version.
```
pyenv virtualenv 3.9.5 <name>
```
3. Activate the environment.
```
pyenv activate <name>
```
4. Install the `requirements.txt` file into the virtual environment.
```
pip install -r requirements.txt
```
5. Download and decompress the file `datafiles.7z` attached in the drive folder.
6. Replace the following folders of the cloned repository with the corresponding decompressed data.
```
Heat Waves Impacts
├── data: Contains the datasets downloaded to develop the project
│   ├── Global Burden of Disease study
│   └── Temperature data
```
7. For each Jupyter notebook available in the `code` folder, change the following path to your local directory where the repository was downloaded.
```
# Main path
root_path = r"C:\Users\Sonita\Documents\KU_Leuven\Subjects\2022-1\Modern Data Analytics\5. New_Project\github"
``` 
8. Run the desired notebook.

## Useful commands

Install requirements file and or update it
```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```

Check current state
```bash
git status
```

Show all branches in repo
```bash
git branch -a
```

New branch (-b creates a new one, without -b you just switch to this branch)
```bash
git checkout -b <new_branch> <parent_branch>
```
example: git checkout -b featureX develop

Push new branch to remote repo
```bash
git push -u origin <new_branch>
```
example: git push -u origin featureX

When finished go to develop branch
```bash
git checkout develop
```

Merge feature into develop
```bash
git merge featureX
```

Delete branch locally
```bash
git branch -d localBranchName
```

Delete branch remotely
```bash
git push origin --delete remoteBranchName
```

Remove last commit
Remove it locally
```bash
git reset HEAD^
```

Remove it remotely (you still have the file in work dir, so it's best to remove repo and start over)
```bash
git push origin +HEAD
```

(later if you want to pull/push)
```bash
git pull

git add .
git commit -m "text"
git push
```
