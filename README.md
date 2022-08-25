### Ticket Trending for RE1 - IN DEVELOPMENT ###

**1. Project Overview**

**1.1. Objectives**

Aim: Decision-making in the RE1 squad is data driven.

Our role in research support requires us to understand the recurrence of issues within the platform we are supporting. In order to do this, it would be informative to capture accurate information on the:

Types of issues being raised (i.e. software installs, service requests, research enquiries...) 
Types of assignees that action these issues
Subject topics being tackled 

This information will allow us to identify the most common pain-points in our users' RE experience and proactively allocate our time and resources accordingly. If we receive an increase in tickets relating to a particular workflow, for example, our bioinformaticians may prioritise workflow improvements in their sprint work. 

**Note: This project was developed by Alexander Ho (Bioinformatician in the RE1 squad, reachable on Slack or by email: alexander.ho@genomicsengland.co.uk)**

**1.2. General approach**

This project has led to the creation of a python script classifier that groups Jira Service Desk (Jira SD) tickets by topic. There are many out-of-the-box "Topic Modelling" packages that can perform this task (see LDA and BERTopic for example), however such methods do not necessarily group tickets into topics that are meaningful for the RE1 squad and the service we provide. The solution to this problem is to write a bespoke Topic Modelling classifier that follows similar logic as existing packages, but allows for the flexibility of choosing the topics. For every ticket, the classifier code calculates TF-IDF embeddings for each key word, calculates the total weight of each topic, and chooses the topic label with the highest weight. This labelling system can be used in conjunction with metrics such as ticket creation dates to track topics over time.

**1.3. Model Validation**

An iterative approach of validation and improvement has been used to drive improvements to the ticket trending classifier. The approach taken was as follows:

      1. Output RE1 tickets from the first 10 sprints of 2022 from Jira SD as CSV
      2. Run the classifier
      3. Compare topic chosen by the model to topic chosen by me
      4. Calculate the % accuracy
      5. Identify ticket case studies where I did not agree with the classifier
      6. Make amendments to the key word dictionaries and classifier logic 
      7. Add or remove key words
      8. Adjust preprocessing of the free text fields 
      9. Generate next version of the model

Results: Version 1 = 72% accurate, Version 2 = 86% accurate, Version 3 = 87% accurate

This process is by no means perfect, with genuine concerns raised about overfitting and unconscious biases.

Overfitting concerns: Testing on the same dataset each time means that adjustments are tailored to this data and not necessarily others.

Unconscious bias: As I am making the improvements and also performing the validations, there is a risk that I might unconsciously assume the model          will improve (and not get worse) and thus agree more with newer model versions.

To address these potential problems, independent validations will now take place with help from other BRS members.

**1.4. Topics currently being tracked**

_Workflow_:   Help with BRS workflows and example scripts provided in the user guide

_Analysis tooling_:   Problems using bioinformatic analysis tools e.g. VEP

_Python support_:  Help with the python language, software and commonly used packages

_R support_:   Help with the R language, software and commonly used packages

_Memory issues_:   Issues relating to memory problems including user capping

_Access issues_:   Problems accessing files/folders, requests to move/copy/delete them

_LabKey_:   Issues with LabKey app, LabKey tables, or the LabKey APIs

_Inuvika apps_:   Relating to IVA, PX, DD, rocket chat etc. in the RE

_Airlock or whitelist_:   Questions about data import and export, requests for whitelisting

_Log in issues_:   Problems logging into the Inuvika RE

_Data queries_:   Data availability / requests for more information about our data

_User guide_:   Questions about our documentation

_HPC usage_:   Best practices using the HPC, node speeds etc.

_Job submission_:   Issues using LSF, working with different queues, submission scripts

_Engineering apps_:   Problems with apps commonly used by RE1 engineers

_Onboarding_:   Relating to onboarding processes and new users

_Microsoft_:   Problems with the Microsoft office apps in the RE

_Performance issues_: Observations that the Research Environment or HPC is running slowly.

**2. How do I run the classifier?**

**2.1. Required files**

topic_model_classifier.py:
Python script that accepts a Jira SD CSV file as an input, processes the free text fields to determine the topic present, and outputs a labelled TSV with all other fields retained. 

2021_training_data.csv:
CSV file containing all Jira SD tickets assigned to the RE1 squad between 01-01-2021 and 31-12-2021, used as training data to calculate key word frequencies.

(Input file) Jira SD exported CSV to be labelled:
Search for issues → Project = GEL Service Desk, Tribe/Squad = Research Ecosystem: RE 1.0 Squad, Created date = Between 01/01/2022 and CURRENT DATE → Export CSV (all fields)

**2.2. Classifier logic**

Follow these instructions to run the classifier:

      1. (optional) Optimise input files.
      2. Adapt the script topics and keywords according to requirements (see below for advice).
      3. Create training data that is representative of the data (historical tickets allocated to a given squad, for example).
      4. Create test data i.e. the data to be labelled with topics.
      5. Adjust file paths in topic_model_classifier.py so the script can find the required files and write the output file to the correct directory.
      6. Run topic_model_classifier.py using Python >= 3.0

**3. How can I adapt the script to capture different topics/keywords?**

Topics:
      - Add or remove Topic/Key Word lists 
      - Edit topic_model() and classifier() functions to include/remove reference to the new lists.
      
Key words:
      - Add or remove key words from each Topic/Key Word list.
      
Other modifications:
      - For adaptations outside of the RE1 squad, edit "Assignees" dictionary as necessary.
      - To tinker with the preprocessing (i.e. lemmatisation, handling of punctuation etc.) you may edit the preprocess() function.
