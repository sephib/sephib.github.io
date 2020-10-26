title: First Post on My Sweet New Blog
date: 2020-07-08
author: Sephi Berry

# Getting started with my online blogging   

This is my first post on my new blog.  
While not super informative it should convey my sense of excitement and eagerness to engage with you,
the reader!

## Publish workflow
1. make changes
2. save
3.1. comment # SITEURL = 'http://sephib.github.io'  
3.2. pelican content -o output  

3.3  check in draft ->  If local server not running - pelican --listen  

4. Publish  
4.1    uncomment # SITEURL = 'http://sephib.github.io'  
4.3    pelican content -o output  
    4.2 ghp-import output -b gh-pages -r https://github.com/sephib/sephib.github.io  
    4.2 git push git@github.com:sephib/sephib.github.io.git gh-pages:master  
