Ticket Trending for RE1

Project Overview: 

Objectives

Aim: Decision-making in the RE1 squad is data driven.

Our role in research support requires us to understand the recurrence of issues within the platform we are supporting. In order to do this, it would be informative to capture accurate information on the:

Types of issues being raised (i.e. software installs, service requests, research enquiries...) 
Types of assignees that action these issues
Subject topics being tackled 

This information will allow us to identify the most common pain-points in our users' RE experience and proactively allocate our time and resources accordingly. If we receive an increase in tickets relating to a particular workflow, for example, our bioinformaticians may prioritise workflow improvements in their sprint work. 

Note: This project was developed by Alexander Ho (Bioinformatician in the RE1 squad, reachable on Slack or by email: alexander.ho@genomicsengland.co.uk) 

General approach

This project has led to the creation of a python script classifier that groups Jira Service Desk (Jira SD) tickets by topic. There are many out-of-the-box "Topic Modelling" packages that can perform this task (see LDA and BERTopic for example), however such methods do not necessarily group tickets into topics that are meaningful for the RE1 squad and the service we provide. The solution to this problem is to write a bespoke Topic Modelling classifier that follows similar logic as existing packages, but allows for the flexibility of choosing the topics. For every ticket, the classifier code calculates TF-IDF embeddings for each key word, calculates the total weight of each topic, and chooses the topic label with the highest weight. This labelling system can be used in conjunction with metrics such as ticket creation dates to track topics over time.

Model Validation

An iterative approach of validation and improvement has been used to drive improvements to the ticket trending classifier. The approach taken was as follows:

Output RE1 tickets from the first 10 sprints of 2022 from Jira SD as CSV
Run the classifier
Compare topic chosen by the model to topic chosen by me
Calculate the % accuracy
Identify ticket case studies where I did not agree with the classifier
Make amendments to the key word dictionaries and classifier logic 
Add or remove key words
Adjust preprocessing of the free text fields 
Generate next version of the model

Results: Version 1 = 72% accurate, Version 2 = 86% accurate, Version 3 = 87% accurate

This process is by no means perfect, with genuine concerns raised about overfitting and unconscious biases.

Overfitting concerns: Testing on the same dataset each time means that adjustments are tailored to this data and not necessarily others.

Unconscious bias: As I am making the improvements and also performing the validations, there is a risk that I might unconsciously assume the model will improve (and not get worse) and thus agree more with newer model versions.

To address these potential problems, independent validations will now take place with help from other BRS members.

Topics currently being tracked

Workflow:   Help with BRS workflows and example scripts provided in the user guide

Analysis tooling:   Problems using bioinformatic analysis tools e.g. VEP

Python support:  Help with the python language, software and commonly used packages

R support:   Help with the R language, software and commonly used packages

Memory issues:   Issues relating to memory problems including user capping

Access issues:   Problems accessing files/folders, requests to move/copy/delete them

LabKey:   Issues with LabKey app, LabKey tables, or the LabKey APIs

Inuvika apps:   Relating to IVA, PX, DD, rocket chat etc. in the RE

Airlock or whitelist:   Questions about data import and export, requests for whitelisting

Log in issues:   Problems logging into the Inuvika RE

Data queries:   Data availability / requests for more information about our data

User guide:   Questions about our documentation

HPC usage:   Best practices using the HPC, node speeds etc.

Job submission:   Issues using LSF, working with different queues, submission scripts

Engineering apps:   Problems with apps commonly used by RE1 engineers

Onboarding:   Relating to onboarding processes and new users

Microsoft:   Problems with the Microsoft office apps in the RE

Performance issues: Observations that the Research Environment or HPC is running slowly.

How do I run the classifier?
Required files
topic_model_classifier.py
Python script that accepts a Jira SD CSV file as an input, processes the free text fields to determine the topic present, and outputs a labelled TSV with all other fields retained. 
2021_training_data.csv
CSV file containing all Jira SD tickets assigned to the RE1 squad between 01-01-2021 and 31-12-2021, used as training data to calculate key word frequencies.
(Input file) Jira SD exported CSV to be labelled
Search for issues → Project = GEL Service Desk, Tribe/Squad = Research Ecosystem: RE 1.0 Squad, Created date = Between 01/01/2022 and CURRENT DATE → Export CSV (all fields)
Classifier logic

Step-by-step guide

Follow these instructions to run the classifier:

(optional) Optimise input files.
Adapt the script topics and keywords according to requirements (see below for advice).
Create training data that is representative of the data that the classifier will run on (historical tickets allocated to a given squad, for example).
Create test data i.e. the data to be labelled with topics.
Adjust file paths in topic_model_classifier.py so the script can find the required files and write the output file to the correct directory.
Run topic_model_classifier.py using Python >= 3.0
How can I adapt the script to capture different topics/keywords?
Topics
Add or remove Topic/Key Word lists 
Edit topic_model() and classifier() functions to include/remove reference to the new lists.
Key words
Add or remove key words from each Topic/Key Word list.
Other modifications
For adaptations outside of the RE1 squad, edit "Assignees" dictionary as necessary.
To tinker with the preprocessing (i.e. lemmatisation, handling of punctuation etc.) you may edit the preprocess() function.
