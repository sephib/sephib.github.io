title: My 2cents reviewing an academic project
date: 2020-12-21
author: Sephi Berry

# Background

Recently we had a closer to an R&D project with a prominent University. Although the results of the project were insightful and possibly applicable to our organization, the processes that the academic R&D team used seemed lacking.  

In this post I whish to highlight some simple steps that can assist in running a DS project (from the initiation until the delivery).  

I'm not going to go into the Project Management aspects but rather some tools and tips for any DS project.

# Setup
1.  Using a [CookieCutter](https://cookiecutter.readthedocs.io/en/latest/installation.html) for project structure.  
    Although this team included MSc. and PhD. students that are running multiple collaborative projects, they did not have a convention for a project structure. While reviewing the deliveries we needed to contact several team members in order to find a specific file. Working with a known template allows all team members to easily save files in designated folders and easily locate files form any project.  
    The template that is used is not really the issue - we use this [Data Science]((https://drivendata.github.io/cookiecutter-data-science/)) template, which sometimes is an over-kill for a simple project, but normally most of the structure is used.  

2. GIT (!@$#%)  
   Yes - still in the year 2020 - teams run projects without a source control! The entire project was offline - so the team thought that they did not need one. How difficult is it to [set up a local git server](https://www.linux.com/training-tutorials/how-run-your-own-git-server/)? Although we did not have a failing disc, we did loose a  specific file that somehow went missing...
   
# Running 
1. CI/CD (low-tec  solution)   
   This one is a bit more tricky.  CI/CD is a must these days for any company who is shipping any product, but what about for a `Data Science` team? Recently our team decided on a simple CI/CD for our Jupyter Notebooks - which include a `kernel restart run all cells`. This solution allows for picking up any notebook and allowing knowing that what ever inside the notebook can run without errors. Obviously this can be improved by:  
   * Removing functions into a separate  `.py` file, leaving the notebook clean and more readable. 
   * Complement the notebooks with a `README` file describing the general process and specifically the data input/output files. Once the project is mature you can upgrade the pipeline into a designated framework such as [dagster](https://dagster.io/)
  
2. Monitoring experiments
   As scientists - we all should understand MLFlow

# Extras
1. Tests
2. Agile


## Publish workflow
1. Edit & save changes to file
2. To view on local computer run `make html` followed by `make serve` 
3. Commit changes when necessary (on the `dev branch`)
4. Finally when ready you can run `make publish` & `make github` to push the changes to the `github.io` site

