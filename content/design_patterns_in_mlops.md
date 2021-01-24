Title: Design patterns in ML and MLops
Date: 2021-01-24  
Author: Sephi Berry  
Tags: python mlops
Summary: Design patterns in MLops, pipelines are core for a successful project
Category: posts
status: draft

# Design patterns in Machine Learning

Listening to [Sara Robinson](https://www.linkedin.com/in/sara-robinson-40377924/) on the [MLOps.community podcast](https://podcastaddict.com/episode/117142559), some issues came out as they relate to our growing industry in ML/AI in general and specifically in Data Engineering realm. Although I have not yet read the book, I'm allowing myself to reflect on what I understood from the episode. There are many issues discussed in the book, fortunately they decided to speak about pipelines, which is dear to my hart - since I believe that it is a key issue for successful ML projects.

As an industry, we are still evolving and best practices are still emerging. Saying that - there are many simple solutions and practices from project management and software development that can easily put an ML project on the right track. Identifying the business values that are currently most relevant are a key component when understanding the various trade offs in the engineering processes.

We too enjoy the flexibility of jupyter notebooks, but I disagree with the what Sara said about when to transition from a jupyter notebook to a more structure pipeline. Working methodologically with templates and clear inputs and outputs for each notebook should be implemented from day one. Breaking up notebooks for each step and writing down the logical stages in a markdown file is a key component for saving time and for successful collaboration with any team member. This is even true for yourself - there is nothing better then returning after a weekend to a project and getting up running within a few minutes.  
One tool that I have lately enjoyed using is [scikit-lego](https://scikit-lego.netlify.app/pandas_pipeline.html), a great library that allows for easily structuring various processes while exploring and managing data within a ML project.

Finally, I totally agree with the excitement that was conveyed by the participant with the understanding that the MLops field is still growing in many directions and understanding that part of the attraction in the field is that we are able to experiment with different methodologies while learning new libraries and designs as we mature the industry. 
