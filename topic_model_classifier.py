#python version = 3.9.1

### IMPORT STATEMENTS ###

import sys
import os
import re
import pandas as pd
import numpy as np

### REQUIRED FILE PATHS ###

input_file = os.path.abspath('../jira_sd/dashboard/22Aug22_export.csv')
training_data_source = os.path.abspath('../repo/2021_training_data.csv')

### SET TOPICS AND KEY WORDS ###

workflow = ['workflow', 'gene variant', 'genevariant', 'gv', 'aggregate variant testing', 'avt', 'functional annotation', 'svcnvworkflow', 'svcnv', 'gwas', 'phewas', "workflow query", "extract variants by coordinate", "results", "svs cnvs for a specific gene", "stdout", "stderr", "analysis scripts"]
log_in_issues = ['log in', 'login', 'grey', 'white', 'into inuvika', 'into research environment', "load research environment", "session expired", "statuspage", "status page", "desktop"]
data_queries = ["sample variant", "discrepancy", "maf", "canvas", "manta", "dragen", "clinvar", "variants", "tiering data", "tiered data", "tier", "tiering", "data import", "database", "data resources", "external data", "data", "genome build", "cohort", "data source", "hpo terms", "data release", "gms", "codes", "where can I find", "ploidy", "location", "allele freq", "reference_genome", "table", "pilot", "library prep"]
analysis_tooling = ["bcftools", "bcf tools", "grep", "vep", "ensembl", "annovar", "cadd", "sigprofiler", "compound het", "analysis", "analysis tool", "hla variant", "annotation", "vep annotation", "plink", "gnomad", "principle component", "aggv", "tabix", "maf", "hla typer", "hlatyper", "exomiser"]
python_support = ['python', ' pip ', 'jupyter', 'jupyter lab', 'jupyter notebook', 'jupyterlabs', "pandas", "numpy", "conda environment", "conda env", "python api", "python channel"]
r_support = ['r studio', 'rstudio', ' r ', 'r\s\d.+', 'CRAN', 'devtools', 'bioconductor', "library", "biocmanager", "rlabkey", "libpath", "r package", "r channel"]
memory_issues = ['memory', 'exceed', 'memory limit', "memory issue", 'storage limit', 'storage', 'capping', 'resource capping', "no space", "no space left", "space limitation"]
access_issues = ["ad group", "permission", "folder", "directory", "access", "set permission", "can't access", "cannot access", "can not access", "can't see", "can not see", "no longer see", "ownership", "change of ownership", "transfer", "change ownership", "move", "moving files", "access issues", "unavailable", 'delete', 'copy', 'copied', "missing"]
labkey = ["labkey", "lab key", "labkey api", "lab key api", "labkey table", "participant id", "table"]
airlock_or_whitelist = ['airlock', 'air lock', 'whitelist', "export", "exportation", "exports", "results", "outside re", "out re", "file request", "web page"]
user_guide = ['documentation', 'user guide', "gere", "confluence", "research help"]
other_inuvika_apps = ['participant explorer', 'data discover', ' iva ', 'rocket chat', "rocketchat", 'panelapp', "panel app", 'igv browser', 'vs code', 'vscode', "application", "rstudio", "text editor", "launch", "kibana", "desktop application", 'gvim', 'pdf viewer', 'libre', 're messages', 'file manager', 'firefox', 'git gui', 'open targets', 'atom']
engineering_software = ['datadog', 'jenkins']
hpc_usage = ["hpc", "node", "queue", "pending", "nodes", "hpc slow", "run slow", "running_slow", "helix", "log in node", "ssh", "cluster"]
job_submission = ["lsf", "pending", "lsf memory usage", "array", "run a script", "run scripts", "submit", "queue", "bsub", "bjob", "cluster"]
onboarding = ["new starter", "onboarding"]
microsoft = ["microsoft", "microsoft office", "excel", "power point", "powerpoint", "microsoft excel", "microsoft word"]
performance_issues = ["running slow", "running slowly", "incredibly slow", "frozen"]

### DICTIONARIES OF RE1 SQUAD ROLES ###

re1_squad = {'brs': ['aho', 'mvizueteforster', 'rbevers'],
            'sys_admin': ['psammarco1', 'nmcginness'],
            'engineer': ['omcpheely', 'yagrawal', 'parunachalam1', 'kdurotoye'],
            'developer': ['mscheepmaker', 'rrees'],
            'general_re1': ['nbagga', 'ssehgal', 'aneed'],
            'sda': ['akanagaratnam', 'clalji', 'cregalado', 'cchristofi', ],
            'airlock': ['podonovan1'],
            'unassigned': ['', ' ', 'Unassigned']}

### FUNCTIONS ###

def preprocess(text):

    ''' Function to clean raw text fields, retaining only letters and underscores (_ is required to recognise some phrases in context)
        INPUT: e.g. hello 1903 there, how/are/you?
        OUTPUT: e.g. hello there how are you
    '''

    #Regex to retain only letters and underscores, convert all words to lower case
    letters_only_text = re.sub("[^a-zA-Z|_]", " ", str(text))
    words = letters_only_text.lower()

    return words


def topic_model():

    ''' Function to load the 2021 training data, clean the free text fields, and calculate key word frequencies.
        INPUT: training data CSV with 'Description' and 'Summary' columns containing free text
        OUTPUT: "Ratios" table, each row is a key words, "Ratios" contains frequency of each key word per ticket, other columns contain presence/absense of key words in each topic
    '''

    #Load training data and remove software requests
    training_data = pd.read_csv(training_data_source)
    training_data = training_data[training_data['Issue Type'] != 'Software Request']

    #Preprocess text fields
    training_data['processed_desc'] = training_data['Description'].apply(preprocess)
    training_data['processed_sum'] = training_data['Summary'].apply(preprocess)

    #Concatenate the two free test fields
    training_data['concatenated_text'] = training_data['processed_sum'] + ' ' + training_data['processed_desc']

    #Create table of key word frequency across the training data
    term_dictionary = dict()
    for keyword in (workflow + log_in_issues + data_queries + analysis_tooling + python_support + r_support + memory_issues + access_issues + labkey + airlock_or_whitelist + user_guide + other_inuvika_apps + engineering_software + hpc_usage + job_submission + onboarding + microsoft + performance_issues):
        term_dictionary[keyword] = sum(training_data.concatenated_text.str.count(keyword))

    total_term_count = sum(term_dictionary.values())

    ratio_dictionary = dict()
    for keyword in (workflow + log_in_issues + data_queries + analysis_tooling + python_support + r_support + memory_issues + access_issues + labkey + airlock_or_whitelist + user_guide + other_inuvika_apps + engineering_software + hpc_usage + job_submission + onboarding + microsoft + performance_issues):
        ratio_dictionary[keyword] = term_dictionary[keyword]/total_term_count

    Ratios = pd.DataFrame.from_dict(ratio_dictionary, orient = 'index')
    Ratios = Ratios.rename(columns = {0: 'Ratios'})

    w_ratio = Ratios.index.isin(workflow)
    Ratios['workflow'] = w_ratio

    li_ratio = Ratios.index.isin(log_in_issues)
    Ratios['log_in_issues'] = li_ratio

    dq_ratio = Ratios.index.isin(data_queries)
    Ratios['data_queries'] = dq_ratio

    at_ratio = Ratios.index.isin(analysis_tooling)
    Ratios['analysis_tooling'] = at_ratio

    ps_ratio = Ratios.index.isin(python_support)
    Ratios['python_support'] = ps_ratio

    rs_ratio = Ratios.index.isin(r_support)
    Ratios['r_support'] = rs_ratio

    mi_ratio = Ratios.index.isin(memory_issues)
    Ratios['memory_issues'] = mi_ratio

    ai_ratio = Ratios.index.isin(access_issues)
    Ratios['access_issues'] = ai_ratio

    l_ratio = Ratios.index.isin(labkey)
    Ratios['labkey'] = l_ratio

    aow_ratio = Ratios.index.isin(airlock_or_whitelist)
    Ratios['airlock_or_whitelist'] = aow_ratio

    ug_ratio = Ratios.index.isin(user_guide)
    Ratios['user_guide'] = ug_ratio

    oia_ratio = Ratios.index.isin(other_inuvika_apps)
    Ratios['other_inuvika_apps'] = oia_ratio

    es_ratio = Ratios.index.isin(engineering_software)
    Ratios['engineering_software'] = es_ratio

    hu_ratio = Ratios.index.isin(hpc_usage)
    Ratios['hpc_usage'] = hu_ratio

    js_ratio = Ratios.index.isin(job_submission)
    Ratios['job_submission'] = js_ratio

    o_ratio = Ratios.index.isin(onboarding)
    Ratios['onboarding'] = o_ratio

    m_ratio = Ratios.index.isin(microsoft)
    Ratios['microsoft'] = m_ratio

    perf_ratio = Ratios.index.isin(performance_issues)
    Ratios['performance_issues'] = perf_ratio

    Ratios = Ratios[Ratios.Ratios > 0]

    return Ratios


def get_assignee_role(username, input_dict):

    ''' Function to convert individual assignee information (usernames) to their role in the squad.
        INPUT: Username, Dictionary of dict[job_role] = [list, of, usernames]
        OUTPUT: Job role within the squad, or "outside_re1" if the username is not found in the dictionary.
    '''

    match = 0
    for k, v in input_dict.items():
        if username in v:
            match += 1
            return k
    if match < 1:
        return 'outside_re1'


def classifier(row, Ratios, squad_dict):

    ''' Function to process each ticket (row): calculate TF-IDF ratios for each key word, calculate total score for each topic, choose best topic label.
        INPUT: Row of Jira SD output CSV containing 'Issue Type' column, 'concatenated' column (preprocessed free text), "Ratios" table
        OUTPUT: Most likely topic label for the ticket
    '''

    #Software requests and Research enquiries are labeled exactly as is
    if row['Issue Type'] != 'Software Request' and row['Issue Type'] != 'Research Enquiries':

        #Count key words present in the ticket
        count_dict = {}
        paragraph = row['concatenated']
        for keyword in list(Ratios.index):
            counts = paragraph.count(keyword)
            if counts > 0:
                count_dict[keyword] = counts

        #Append this count information to the Ratios dataframe generated for the training data
        #Calculate the Weighted Ratio of each term
        #Capture results in topic_list

        topic_list = []

        if len(count_dict) > 0:

            #Pull the TF-IDF Ratios from the Ratios table. This will weigh each matching word accordingly
            sent_df = Ratios.join(pd.DataFrame.from_dict(count_dict, orient = 'index'), how = 'inner')
            sent_df = sent_df.rename(columns = {0: 'Counts'})
            divide = (1/sent_df['Ratios'])
            Ratio_sum = ((1/sent_df['Ratios'])*sent_df['Counts']).sum()
            sent_df['Weighted_Ratio'] = (1/(sent_df['Ratios'])*sent_df['Counts'])/Ratio_sum

            #Aggregate the terms into the topics specified
            sent_gb = sent_df.groupby(['workflow', 'log_in_issues', 'data_queries', 'analysis_tooling', 'python_support', 'r_support', 'memory_issues', 'access_issues', 'labkey', 'airlock_or_whitelist', 'user_guide', 'other_inuvika_apps', 'engineering_software', 'hpc_usage', 'job_submission', 'onboarding', 'microsoft', 'performance_issues'], as_index = False)['Weighted_Ratio'].sum()

            #Append these to the original lists
            if sent_gb['workflow'].any() == True:
                topic_list.append(sent_gb[sent_gb['workflow'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['log_in_issues'].any() == True:
                topic_list.append(sent_gb[sent_gb['log_in_issues'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['data_queries'].any() == True:
                topic_list.append(sent_gb[sent_gb['data_queries'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['analysis_tooling'].any() == True:
                topic_list.append(sent_gb[sent_gb['analysis_tooling'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['python_support'].any() == True:
                topic_list.append(sent_gb[sent_gb['python_support'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['r_support'].any() == True:
                topic_list.append(sent_gb[sent_gb['r_support'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['memory_issues'].any() == True:
                topic_list.append(sent_gb[sent_gb['memory_issues'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['access_issues'].any() == True:
                topic_list.append(sent_gb[sent_gb['access_issues'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['labkey'].any() == True:
                topic_list.append(sent_gb[sent_gb['labkey'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['airlock_or_whitelist'].any() == True:
                topic_list.append(sent_gb[sent_gb['airlock_or_whitelist'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['user_guide'].any() == True:
                topic_list.append(sent_gb[sent_gb['user_guide'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['other_inuvika_apps'].any() == True:
                topic_list.append(sent_gb[sent_gb['other_inuvika_apps'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['engineering_software'].any() == True:
                topic_list.append(sent_gb[sent_gb['engineering_software'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['hpc_usage'].any() == True:
                topic_list.append(sent_gb[sent_gb['hpc_usage'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['job_submission'].any() == True:
                topic_list.append(sent_gb[sent_gb['job_submission'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['onboarding'].any() == True:
                topic_list.append(sent_gb[sent_gb['onboarding'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['microsoft'].any() == True:
                topic_list.append(sent_gb[sent_gb['microsoft'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

            if sent_gb['performance_issues'].any() == True:
                topic_list.append(sent_gb[sent_gb['performance_issues'] == True].reset_index().iloc[0]['Weighted_Ratio'])
            else:
                topic_list.append(0)

        else:
            topic_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        #Add columns containing topic weights
        row['workflow_weight'] = topic_list[0]
        row['log_in_issues_weight'] = topic_list[1]
        row['data_queries_weight'] = topic_list[2]
        row['analysis_tooling_weight'] = topic_list[3]
        row['python_support_weight'] = topic_list[4]
        row['r_support_weight'] = topic_list[5]
        row['memory_issues_weight'] = topic_list[6]
        row['access_issues_weight'] = topic_list[7]
        row['labkey_weight'] = topic_list[8]
        row['airlock_or_whitelist_weight'] = topic_list[9]
        row['user_guide_weight'] = topic_list[10]
        row['other_inuvika_apps_weight'] = topic_list[11]
        row['engineering_software_weight'] = topic_list[12]
        row['hpc_usage_weight'] = topic_list[13]
        row['job_submission_weight'] = topic_list[14]
        row['onboarding_weight'] = topic_list[15]
        row['microsoft_weight'] = topic_list[16]
        row['performance_issues_weight'] = topic_list[17]

        #Topic with the highest weight is the assigned label
        labels = ['workflow', 'log_in_issues', 'data_queries', 'analysis_tooling', 'python_support', 'r_support', 'memory_issues', 'access_issues', 'labkey', 'airlock_or_whitelist', 'user_guide_or_confluence', 'inuvika_apps', 'engineering_software', 'hpc_usage', 'job_submission', 'onboarding', 'microsoft', 'performance_issues']
        max_value = max(topic_list)
        if max_value > 0.5:
            max_index = topic_list.index(max(topic_list))
            best_label = labels[max_index]
        else:
            best_label = 'topic_unclear'
        row['predicted_label'] = best_label

    #We don't bother calculating weights for Software Requests
    elif row['Issue Type'] == 'Software Request':

        row['workflow_weight'] = 0
        row['log_in_issues_weight'] = 0
        row['data_queries_weight'] = 0
        row['analysis_tooling_weight'] = 0
        row['python_support_weight'] = 0
        row['r_support_weight'] = 0
        row['memory_issues_weight'] = 0
        row['access_issues_weight'] = 0
        row['labkey_weight'] = 0
        row['airlock_or_whitelist_weight'] = 0
        row['user_guide_weight'] = 0
        row['other_inuvika_apps_weight'] = 0
        row['engineering_software_weight'] = 0
        row['hpc_usage_weight'] = 0
        row['job_submission_weight'] = 0
        row['onboarding_weight'] = 0
        row['microsoft_weight'] = 0
        row['performance_issues_weight'] = 0
        row['predicted_label'] = 'software_request'

    #We don't bother calculating weights for Research Enquiries
    elif row['Issue Type'] == 'Research Enquiries':

        row['workflow_weight'] = 0
        row['log_in_issues_weight'] = 0
        row['data_queries_weight'] = 0
        row['analysis_tooling_weight'] = 0
        row['python_support_weight'] = 0
        row['r_support_weight'] = 0
        row['memory_issues_weight'] = 0
        row['access_issues_weight'] = 0
        row['labkey_weight'] = 0
        row['airlock_or_whitelist_weight'] = 0
        row['user_guide_weight'] = 0
        row['other_inuvika_apps_weight'] = 0
        row['engineering_software_weight'] = 0
        row['hpc_usage_weight'] = 0
        row['job_submission_weight'] = 0
        row['onboarding_weight'] = 0
        row['microsoft_weight'] = 0
        row['performance_issues_weight'] = 0
        row['predicted_label'] = 'research_enquiry'

    return row


### MAIN FUNCTION TO RUN ###

def main():

    #Read input data, replace empty cells with Nan
    raw = pd.read_csv(input_file)
    raw.replace(r'^\s*$', np.nan, regex=True)

    #Preprocess free text fields and deidentify assignee information
    raw['preprocessed_desc'] = raw['Description'].apply(preprocess)
    raw['preprocessed_sum'] = raw['Summary'].apply(preprocess)
    raw['concatenated'] = raw['preprocessed_sum'] + (' ') + raw['preprocessed_desc']
    raw['assignee_squad'] = raw['Assignee'].apply(get_assignee_role, input_dict=re1_squad)

    #Classify tickets into tppics
    Ratios = topic_model()
    results = raw.apply(classifier, Ratios=Ratios, squad_dict=re1_squad, axis=1)

    #Write output
    out_path = input_file.replace('.csv', '_labelled.tsv')
    results.to_csv(out_path, sep='\t', index=False)


### RUN SCRIPT ###
if __name__ == "__main__":
    main()
