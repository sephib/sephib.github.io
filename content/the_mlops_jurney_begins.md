Title: The Jurney to ML ops
Date: 2021-07-16
Author: Sephi Berry
Tags: python mlops  
Summary: The stages that our team is taking towards and ML infenstructure
Category: posts  
status: draft


# Outline 
1. Intro
2. Challenges
3. road map
4. tools

# Introduction
Joining [artlist](artlists.io) is a wonderful opportunity for me. Artlist is a fast growing company with many processes that are being developed. The AI team is in the R&D division while we serve a wide range of teams from the marketing to the content curators. In addition there are many data consumers that are our (potential) clients, thus we need to put in-place a ML foundations, that will allow us to iterate in a robust manner when we iterate over the various AI models.

# Challenges
Working in a small team requires to be self sufficient. we need to manage our infrastructure, easily trace our logs and increase collaboration among team mates. This may sound simple and common, but holds many challenges. Here are the core elements that we came up for our team work:

4. Standardize  project structure & development
1. Manage configurations and setting  
2. Unity in logging  
3. CI/CD for development process
5. Standerdize Kubeflow  (Components, usability)

Lets dive into the verious above elements
## Project Structure
Working in a team requires collaboration on many levels. In a software team takes this real collaboration to a higher level, since it requires the ability to easily jump into the creation/ יצירה with minimal friction.
In order to allow for such case it is important to understand the structure of the project, how to execute it and the various elements that can easily allow for contribution. this is crucial for fast iterations and reducing the fear when diving into a colleagues code. Once established, code reviews and other collaboration processes are easier and constructive.

## Kubeflow component
Intro to kubeflow?  

We have strategically decided to go-all-in into the Kubeflow framework for ML processes. I will not elaborate on the framework (see docs link), however for this post all you need to know that there are 3 core elements to Kubeflow:
  1. Components - the basic working unit that runs within a dockerfile
  2. Pipeline - an element for connecting between the components and managing dependencies and artifacts
  3. Kubernetis - the computation framework for running the Components
Put KF diagram 


## We are very hungry - let's eat some cookies
Now that we have our ML framework, we can design our building blocks. Inspired by [scikit-lego](https://scikit-lego.readthedocs.io/en/latest/), we also want to play with lego, lets work on our basic building cube.
The standard lego block is 2 * 3 [image of lego block] - so here are our 6 pillars for our common development:

  1. Mange configuration -
    Sharing the same codebase is obvious with `git` like solutions, however how to manage the configuration is a bit more of an art. This friction point can be both frustrating and potential for leakage of sensitive information  (see also our secrets management solution).
    After reviewing several solutions we landed on [dynaconf](https://dynaconf.readthedocs.io) ![dynacof](https://www.dynaconf.com/img/logo_400.svg?sanitize=true) - and cannot look back. The library is well documented and can be customized to most use cases. Our main twig included incorporating _Pipeline_ configs in addition to the _Component_ configs, so when ever we are building a new project both sets of configs are loaded, the shared configs (pipeline) with the dedicated configs (component). in addition to Pipeline configs
    1. dynaconf
      1. project s
  2. Project structure
    __Lost in Translation__ is a nice film, but cirtanlly not somthing you want to encounter whenever opening a teams project or using a common component. Building a cookiecutter with a boiler plat is a great way to start - but doing so requires a robust project structure. After some experience building some KF components we came up with the following structure.
    1. component structure
      <component_name>-
                        |
                        config
                              |
                              - settings.toml
                              - settings.local.toml
                        src
                            |
                            _ lib
                                |
                                - <lib_files>.py
                            - run.py
                        tests
                            |
                            - test_run.py
                            
    2. project/pipeline structure<>
  src code
  3. Dockerfile
  4. venv
  5. tests
  6. CICD - 
    1. Makefile
    2. 








# Road Map
1. Development 
