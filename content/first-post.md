title: Warming up  - My First  Blog Post
date: 2020-07-08
author: Sephi Berry

# Getting started with my online blogging   

This is my first post on my new blog.  
I hope to be able to share my thoughts and knowledge in the various tech stacks that I'm involved in.

I'm going run on Pelican (a python static web site generator). There are numerous resources on the web - which may conflict with each other. Here is how I boiled it down (while hosting the site on github).  

After setting up your environment (with the required installations)

## Initial setup
After the setup (kickstart setup process)[https://docs.getpelican.com/en/stable/install.html#kickstart-your-site], follow the documentation on (Pelican tips)[https://docs.getpelican.com/en/latest/tips.html#user-pages] section to publish the blog as a `user page`. Create a `dev branch` to commit all the files while the blog itself will be published on the `main branch`.

Edit the `pelicanconf.py` and `publishconf.py` as necessary (this will also depends on the [theme](http://www.pelicanthemes.com/) and [plugin](https://github.com/getpelican/pelican-plugins) that you will be running with).  


## Publish workflow
1. Edit & save changes to file
2. To view on local computer run `make html` followed by `make serve` 
3. Commit changes when necessary (on the `dev branch`)
4. Finally when ready you can run `make publish` & `make github` to push the changes to the `github.io` site

