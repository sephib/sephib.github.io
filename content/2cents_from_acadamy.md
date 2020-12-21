title: My 2cents reviewing an academic project
date: 2020-12-21
author: Sephi Berry

# Background

Recently we had a closer to an R&D project with a prominent University. Although the results of the project were insightful and possibly applicable to our organization, the processes that the academic R&D team used seemed lacking.  

In this post I whish to highlight some simple steps that can assist in running a DS project (from the initiation until the delivery).  

I'm not going to go into the Project Management aspects but rather some tools and tips for any DS project.

## Setup
1.  Using a [cookiecutter](https://drivendata.github.io/cookiecutter-data-science/) for project structure.
    Although this team included MSc. and PhD. students that are running multiple collaborative projects, there was not 

After the setup (kickstart setup process)[https://docs.getpelican.com/en/stable/install.html#kickstart-your-site], follow the documentation on (Pelican tips)[https://docs.getpelican.com/en/latest/tips.html#user-pages] section to publish the blog as a `user page`. Create a `dev branch` to commit all the files while the blog itself will be published on the `main branch`.

Edit the `pelicanconf.py` and `publishconf.py` as necessary (this will also depends on the [theme](http://www.pelicanthemes.com/) and [plugin](https://github.com/getpelican/pelican-plugins) that you will be running with).  


## Publish workflow
1. Edit & save changes to file
2. To view on local computer run `make html` followed by `make serve` 
3. Commit changes when necessary (on the `dev branch`)
4. Finally when ready you can run `make publish` & `make github` to push the changes to the `github.io` site

