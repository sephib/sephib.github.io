Title: My 2cents worth after reviewing an academic project   
Date: 2020-12-21  
Author: Sephi Berry  
Tags: python data_analysis 
Summary: My 2cents after reviewing an academic project   
Category: posts

# Background

Recently we had a completion of an R&D project with a prominent university. Although the results of the project were insightful and possibly applicable to our organization, the workflow that the academic R&D team used seemed inadequate.   

In this post, I wish to highlight some simple steps that can assist in running Data Science (DS) projects (from the initiation until the deployment) by DS teams, especially those working without the support of specialized tools.  

I'm not going to go into the Project Management aspects but rather some tools and tips for any DS project.

# Setup
1.  Using <img src="https://miro.medium.com/max/1200/1*wfMxroB_sHsx06lrreeKew.png" alt="drawing" height="30" href="https://cookiecutter.readthedocs.io/en/latest/installation.html" />  for project structure.  
      
    Although this team included MSc. and PhD. students who are running multiple collaborative projects, they did not have a convention for a DS project structure. While reviewing the deliverables we needed to contact several team members in order to find a specific file. Working with a known template allows all team members to save files easily in designated folders and readily locate files from any project.  
    The template that is used is not really the issue - we use this [Data Science]((https://drivendata.github.io/cookiecutter-data-science/)) template, which sometimes is an "overkill" for  simple projects, but normally most of the structure is used.  

2. Using <img src="https://camo.githubusercontent.com/6eaaae8defc78f268eaf0824350a66a1dfcb6aa77210d3dca069d1d1cefebc53/68747470733a2f2f6769742d73636d2e636f6d2f696d616765732f6c6f676f732f646f776e6c6f6164732f4769742d4c6f676f2d32436f6c6f722e706e67" alt="drawing" height="40" href="https://git-scm.com/"/>  (!@$#%)  
  
   Yes - still in the year 2020 - teams run projects without a version control system! The entire project was offline - so the team thought that they did not need one. How difficult is it to [set up a local git server](https://www.linux.com/training-tutorials/how-run-your-own-git-server/)? Although we did not have a failing disc, we did lose a specific file that somehow went missing...
   
# Running 
1. CI/CD (low-tech  solution)   
   This one is a bit more tricky.  CI/CD is a "must" these days for companies who are shipping a product, but what about for a `Data Science` team? This is even more challenging when using `Jupyter Notebooks` that are not "git friendly".  
   Recently our team decided on a simple CI/CD for our  - which include a `kernel restart run all cells`. This solution allows for picking up any notebook and  knowing that what ever is inside the notebook, and can run without any errors.  
   We supplement this solution with the following procedures:   

     * Removing functions into a separate  `.py` file, leaving the notebook clean and more readable. 
     * Separating **each** notebook as a single step in the analysis pipeline. 
     * Complement a set of notebooks with a `README` file describing the general process and specifically the data input/output files.  
  
    Once the project is mature you can upgrade the pipeline into a designated framework such as [dagster](https://dagster.io/)
  
2. Monitoring experiments  
   As scientists - experimentation and failures are part of our daily life. Working in a systematic manner allows for confidence in the results and for reproducible science.  Stating that _"we checked the various parameters and these values were the best"_ is not the best practice unless these can be easily reviewed and reproduced.   
   Running `print` statements without a central `logging` module is also very problematic. Just being able to run the exact same code and get similar logs is very beneficial for understanding how the project runs etc.      
   During the past years, there are many platform/frameworks that have been developed for managing solutions for ML projects. We have settled on [MLFlow](https://mlflow.org), which allows for ease of installation and use even in an offline environment. 

# Summary  

There are many constraints when running a project. However, some minimal infrastructure can get you a long way. Working without any guidelines will normally lead to chaos and inefficiency, while, at the same time, lowering the quality level of the science and of the project.  
Today, `MLOps` and `DataOps` tools and guidelines are constantly being developed, so I'm sure we will see ease of use and improvements in the coming years. 
