# -*- coding: utf-8 -*-
"""Copy of Test_File_Pre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nrm1ftO6JKkJlmAxsQjFJPOo5wc1L4lF
"""

# Loading some libraries
# This step might takes few mins

# from google.colab import drive
# drive.mount('/content/drive')

# Loading some libraries
# This step might takes few mins

import os 
currentDirectoryPATH = os.path.dirname(os.path.realpath(__file__))

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings(action='ignore')
import collections
from scipy.stats import entropy
import nltk
from nltk.corpus import words, stopwords
nltk.download('words')
nltk.download('stopwords')
# !pip install langid
from langid.langid import LanguageIdentifier, model
import gensim.downloader as api
# !pip install wordninja
import wordninja
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import SVC
# !pip install blosc
# !pip install pickle 

import pickle
import blosc


# !pip install embeddings  # from pypi
# !pip install git+https://github.com/vzhong/embeddings.git  # from github

from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


# !pip install category_encoders==2.0.0
# !pip install -q transformers
# !pip install tensorflow-addons
# !pip install wordninja
# !pip install xlsxwriter

# It takes around 6 GB
from weakref import WeakValueDictionary
from gensim import models
# !pip install gensim # to upgrade version
from gensim.models import Word2Vec
import gensim

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
import sklearn.metrics as metrics

################################################
# Test Results
ACCURACY = 0.0
ERROR_READING = False
ERROR_PATH    = False


###############################################
# Final Features
Col_Features = [ 'index', 'DLength', 'DAlpha', 'DHaveDigits', 'DAllDigits', 'DHaveHyphen', 
                  'DFirstDigit','DLastDigit', 'DVowelRatio', 'DConsonantRatio', 'DHyphenRatio', 'DDigitRatio', 'DShannonEntropy' ,'DWordCount', 
                  'DPCA1', 'DPCA2', 'DPCA3', 'DPCA4', 'DPCA5' ]   # PCA Featurs 
Col_Output  = 'category'

#from gensim.models import Word2Vec

# Load pretrained model (since intermediate data is not included, the model cannot be refined with additional data)

try:
  wv = gensim.models.KeyedVectors.load_word2vec_format(currentDirectoryPATH+'/trained_models/GoogleNews-vectors-negative300.bin', binary=True)
except:
  ERROR_PATH = True
  print('Error reading input data')



IS_DEBUG = True # TO see some log etc

#######################################################################################################################################
# 1- Test File Path
# 2-  Where to store results
# 3 - Model File Path
############################
# Test File paths
############################
# Make sure to change these paths as per server path


##################################################
# INPUT FILE PATH
##################################################
# Give the INPUT FILE PATH

# In google drive, the path start from this:

INPUT_PATH = ''
try:
  INPUT_PATH = currentDirectoryPATH + '/uploads/uploaded_data_file.csv'
except:
  ERROR_READING = True
  print('Error reading input data')


##################################################
# OUTPUT FOLDER PATH
##################################################

# Give the "FOLDER PATH", WHERE you want results (It needed to be folder only --- DONT GIVE FILE NAME)

OUTPUT_FOLDER = ''
try:
  OUTPUT_FOLDER = currentDirectoryPATH + '/results/'
except:
  ERROR_PATH = True
  print('Error reading input data')



##################################################
# SAVED MODEL PATH
##################################################
# make sure to change this path as needed (models are saved in the code shared)

#saved_models_path = '/content/drive/MyDrive/Domain_Name_Prediction_Final/Code/SavedModels/NN_HASHModel/Model_new'

# If you are in computer, it should something like this one:
saved_models_path = currentDirectoryPATH + '/trained_models/'
saved_models_DT = saved_models_path + 'DT_finalized_model.sav'
saved_models_LR = saved_models_path + 'LR_finalized_model.sav'
saved_models_SVC = saved_models_path + 'SVC_finalized_model.sav'


####################################################################################
# Dont worry about these paths, they will use above path to adjust automatically
###################################################################################

# result file will be generated automatically 
file_to_save_results = OUTPUT_FOLDER + 'Results.xlsx'


file_to_save_features = OUTPUT_FOLDER + 'testingdata_prep.xlsx'


# Result File
result_path = OUTPUT_FOLDER
result_path_accuracy = OUTPUT_FOLDER + 'accuracy.png'
result_path_errors = OUTPUT_FOLDER + 'errors.png'
result_path_confusion = OUTPUT_FOLDER + 'confusion.png'

# test file
test_file = INPUT_PATH


data = pd.read_csv(INPUT_PATH, encoding= 'unicode_escape')


# Load feature extraction libraries
# Loading time in seconds
import io  
import matplotlib.pyplot as plt
import nltk.corpus
nltk.download('gutenberg')
nltk.download('genesis')
nltk.download('inaugural')
nltk.download('nps_chat')
nltk.download('webtext')
nltk.download('treebank')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.book import *
from nltk.corpus import brown

english_vocab = set(w.lower() for w in nltk.corpus.words.words())

dist = data.category.value_counts().to_frame().reset_index()
dist['% distribution'] = data.category.value_counts().values/data.shape[0] * 100
dist.columns = ['categories', 'count', '% distribution']
dist


#############

# Extracting the domain name
data['DName'] = data['Domain'].apply(lambda x: x.split('.')[0].lower())

# Extracting the domain extension
data['DExt'] = pd.Series(len(data))  # Initiaze in case we have errors
try:
  data['DExt'] = data['Domain'].apply(lambda x: x.split('.')[1])
except:
  print('data[DExt] issue')

# Counting the number of characters in the domain name
data['DLength'] = data['DName'].apply(lambda x: len(x))

# Extracting all alphabets in the domain name and counting the number of alphabets in the string
data['DAlphaChar'] = data['DName'].apply(lambda x: ''.join(re.findall('[a-zA-Z-]', x)))
data['DAlpha'] = data['DAlphaChar'].apply(lambda x: len(x))

# Are there digits in the domain name
data['DHaveDigits'] = data['DName'].apply(lambda x: 0 if len(re.findall('\d', x)) == 0 else 1)
data['DAllDigits'] = data.apply(lambda x: 1 if len(re.findall('\d', x['DName'])) == x['DLength'] else 0, axis = 1)

# Are there hyphens in the domain name
data['DHaveHyphen'] = data['DName'].apply(lambda x: 0 if len(re.findall('[-]', x)) == 0 else 1)

# Checking if the first character of the domain name is an alphabet or digit: 1 if digit, 0 if alphabet
data['DFirstDigit'] = data['DName'].apply(lambda x: 1 if x[0].isdigit() else 0)

# Checking if the last character of the domain name is an alphabet or digit: 1 if digit, 0 if alphabet
data['DLastDigit'] = data['DName'].apply(lambda x: 1 if x[-1].isdigit() else 0)

# Define UDF to compute the ratio of vowels and consonants relative to the length of alphabets in the domain name
def extract_ratio(x, arg):
  if x['DAlpha'] == 0:
    return 0
  elif arg == 'vowel':
    return len(re.findall('[aeiou]', x['DName']))/x['DLength']
  elif arg == 'cons':
    return len(re.findall('[^aeiou0-9-]', x['DName']))/x['DLength']

# Compute the ratio of vowels to total alphabets (reflects pronouncability)
data['DVowelRatio'] = data.apply(lambda x: extract_ratio(x, 'vowel'), axis = 1)

# Compute the ratio of consonants to total alphabets
data['DConsonantRatio'] = data.apply(lambda x: extract_ratio(x, 'cons'), axis = 1)

# Compute the ratio of underscore
data['DHyphenRatio'] = data.apply(lambda x: len(re.findall('[-]', x['DName']))/x['DLength'], axis = 1)

# Compute the ratio of underscore
data['DDigitRatio'] = data.apply(lambda x: len(re.findall('\d', x['DName']))/x['DLength'], axis = 1)

#################
# define a UDF which computes the shannon entropy of any given string
def shannon_entropy(d_name):
    # count occurence of each character in the string
    xters = collections.Counter([txt for txt in d_name])
    # compute the ratio of each character relative to the length of the string
    dist = [x/sum(xters.values()) for x in xters.values()]
    # compute the entropy
    shan_entropy = entropy(dist, base=2)
 
    return shan_entropy

data['DShannonEntropy'] = data['DName'].apply(lambda x: shannon_entropy(x))
########################

# extract all meaningful words from the domain name if any using the wordninja library
data['DWords'] = data['DAlphaChar'].apply(lambda x: x.split('-') if '-' in x and len(x) > 5 else wordninja.split(x))

# define a function to remove stopwords and single letters from a list of words
def clean_LOW(lst):
  # list of english stop words
  stops = list(set(stopwords.words('english')))
  # list of english alphabets
  alphabets = [chr(x) for x in range(ord('a'), ord('z') + 1)]
  # set of stopwords in list of words
  stops_in_lst = set(lst).intersection(set(stops))
  # set of alphabets in list of words
  remove = set(lst).intersection(set(alphabets).union(set(stops)))
  for i in remove:
    if i in lst:
      lst.remove(i)
  for i in lst:
    if len(i) <= 2:
      lst.remove(i)
  return lst

data['DWords'] = data['DWords'].apply(lambda x: clean_LOW(x))

# count number of meaningful words in the domain name
data['DWordCount'] = data['DWords'].apply(lambda x: len(x))
data['DWordCount'].max()

cnt = data[data['DWordCount'] > 5].shape[0]
print('There are %d domain names in the dataset with 5 or more meaningful words' %cnt)
#######################

# define function to obtain the average vector for each group of words
def vectorize(x):
  vec = np.zeros(300)
  if x['DWords'] == []:
    pass
  else:
    for i in x['DWords']:
      try:
        vec =+ wv2[i]
      except:
        pass
    vec = vec/x['DWordCount']
  return vec

data['DVector'] = data.apply(lambda x: vectorize(x), axis = 1)

data.sample(10)

####################

clean_data = data
print(clean_data.head())

################
# Drop null values if any
print('We have %s rows before dropping null values' % clean_data.shape[0])
clean_data.dropna(subset = ['DName'], inplace = True)
print('We have %s rows after dropping null values' % clean_data.shape[0])
clean_data.isnull().sum()
################

clean_data.drop(['DExt'], axis = 1, inplace = True )
##################

# Here the session crashes due to issue of tolist etc
# decomposing the word vectors from 300 to 5

#print(clean_data['DVector'])

pd.set_option('display.max_columns', None)
clean_data.head(10)


pca = PCA(n_components = 5)
outcome = pca.fit_transform(pd.DataFrame(np.vstack(clean_data['DVector'].values)))
pca_df = pd.DataFrame(data = outcome, columns = ['DPCA1', 'DPCA2', 'DPCA3', 'DPCA4', 'DPCA5'])
pca_df.shape
clean_data.shape
    
###########################
# concatinating the data with the pca columns
all_data = clean_data.reset_index().join(pca_df)
# dropping the original vector column
all_data.drop(['DVector'], inplace = True, axis = 1)
all_data.isnull().sum()

############################
all_data.head()
###########################
# splitting the data into dependent and independent variables

# also dropping text features
X = all_data.drop(['DName', 'DAlphaChar', 'DWords'], axis = 1)

pd.set_option('display.max_columns', None)
X.head(10)
##########################
# For test set we cant drop any columns  

from sklearn.feature_selection import VarianceThreshold

'''
def variance_threshold_selector(data, threshold):
  selector = VarianceThreshold(threshold)
  selector.fit(data)
  return data[data.columns[selector.get_support(indices=True)]]
  
filtered_X = variance_threshold_selector(X, threshold=0.02)
filtered_X.var()
'''

#############################
# scaling the data using a minmaxscaler as we have some negative values in our PCA features

filtered_X = X;
pd.set_option('display.max_columns', None)
filtered_X.head(10)

'''
scaler = MMS(feature_range=(0, 1))
final_X =  scaler.fit_transform(filtered_X)
'''
final_X  = filtered_X [Col_Features]
y        = filtered_X [Col_Output]
##############################

final_X.head()

"""#Load model"""

###########################################
# Load saved models
###########################################

model_loaded_lr = pickle.load(open(saved_models_LR, 'rb'))
#model_loaded_dt = pickle.load(open(saved_models_DT, 'rb'))
#model_loaded_svc = pickle.load(open(saved_models_SVC, 'rb'))

# Make model_Predictions

model_predictions = model_loaded_lr.predict(final_X)
print(model_predictions)

dummy_output = filtered_X
dummy_output ['model_Predictions'] = model_predictions
final_outputs = dummy_output [['Domain', 'category', 'model_Predictions']]
print(final_outputs.head())

for row_index, (input, prediction, label) in enumerate(zip (final_X, model_predictions, y)):
  if prediction != label:
    print('Row', row_index, 'has been classified as ', prediction, 'and should be ', label)

"""## ERRORS (MSE, RMSE, AE) & ACCURACY (precision_score, recall_score, f1_score)

---


"""

# confusion matrix for NN- hash encoding
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

print(metrics.classification_report(y, model_predictions))
matrix = confusion_matrix(y, model_predictions)
print(matrix)

def categorize_prediction_level(actual, predicted):
  df = pd.DataFrame()
  df['actual'] = actual
  df['predicted'] = predicted
  df['difference'] = (df['actual'] - df['predicted']).abs()
  return df

np.unique(model_predictions, return_counts=True)
error_level_df = categorize_prediction_level(y, model_predictions)
error_level_df.head()


#Counting errored values
error_level_df['difference'].value_counts()

errored_model_predictions = error_level_df[error_level_df["difference"] >= 1]

errored_model_predictions_1 = error_level_df[ ( (error_level_df["difference"] > 1) & (error_level_df["difference"] <=2) ) ]
errored_model_predictions_2 = error_level_df[ ( (error_level_df["difference"] > 2) & (error_level_df["difference"] <=3) ) ]
errored_model_predictions_3 = error_level_df[ ( (error_level_df["difference"] > 3) & (error_level_df["difference"] <=4) ) ]
errored_model_predictions_4 = error_level_df[ ( (error_level_df["difference"] > 4) & (error_level_df["difference"] <=5) ) ]


total_errored_model_predictions = len(errored_model_predictions)
total_errored_model_predictions_1 = len(errored_model_predictions_1)
total_errored_model_predictions_2 = len(errored_model_predictions_1)
total_errored_model_predictions_3 = len(errored_model_predictions_1)
total_errored_model_predictions_4 = len(errored_model_predictions_1)

print('total errors = ', total_errored_model_predictions )
print('total errors with margin 1 = ', total_errored_model_predictions_1 )
print('total errors with margin 2= ', total_errored_model_predictions_2 )
print('total errors with margin 3 = ', total_errored_model_predictions_3 )
print('total errors with margin 4 = ', total_errored_model_predictions_4 )
print(errored_model_predictions)


# Save in figure
all_lables = ['Error 1','Error 2','Error 3','Error 4','Error 5' ]
all_err = [total_errored_model_predictions, total_errored_model_predictions_1, total_errored_model_predictions_2, total_errored_model_predictions_3, total_errored_model_predictions_4]
plt.bar(all_lables, all_err)
plt.xlabel("Errors' Margin")
plt.ylabel("Total COunt")
plt.title('Counting Total Errors with their deviation', fontsize=18)
plt.savefig(result_path_errors)

#########################################
# Get Wrong model_predictions
#########################################
All = []
All_Wrong  = []

# For wrong only
for row_index, (input, prediction, label) in enumerate(zip (filtered_X, model_predictions, y)):
  if prediction != label:
    try:
      msg = 'Row', row_index, filtered_X['Domain'][row_index], ' has been classified as ', prediction, 'and should be ', label
      print(msg)
      All_Wrong.append(msg)
    except:
      print('index out of range')

# For all
for row_index, (input, prediction, label) in enumerate(zip (X, model_predictions, y)):
  try:
    msg = 'Row', row_index, filtered_X['Domain'][row_index], ' has been classified as ', prediction, 'and should be ', label
    print(msg)
    All.append(msg)
  except:
    print('host not found')

df_all_erros = pd.DataFrame  (All_Wrong)  
df_all_predictions = pd.DataFrame  (All)

from sklearn.metrics import mean_squared_error
import math
 
MSE = mean_squared_error(y, model_predictions)
 
print("Mean Square Error:\n")
print(MSE)

RMSE = math.sqrt(MSE)
print("\nRoot Mean Square Error:\n")
print(RMSE)

acc = accuracy_score(y, model_predictions)
ACCURACY = acc

##################################
# For printing into sheets
##################################

message = "=============Errors============= \n\n\n"
mse_data = "Mean Square Error:        "+ str(MSE) + "\n"
rmse_data = "Root Mean Square Error:  "+ str(RMSE) + "\n"
acc_data = "Accuracy: " + str(acc) + "\n"
all_data = message + mse_data + rmse_data + acc_data 
all_data = all_data + "\n ==============================\n"

df_error = pd.read_csv(io.StringIO(all_data), sep=";")

data_x = ['MSE', 'RMSE']
data_errors = [MSE, RMSE]

fig, axs = plt.subplots(1,2)
fig.suptitle('Errors and Accuracy', fontsize=18)
axs[0].bar(data_x, data_errors)
axs[1].bar('Accuracy', acc)

plt.xlabel("Metrics")
plt.ylabel("Value")
plt.savefig(result_path_accuracy)

# Calculate the confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report #  for NN- hash encoding


conf_matrix = confusion_matrix(y_true=y, y_pred=model_predictions)
#
# Print the confusion matrix using Matplotlib
#
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('model_Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()
fig.savefig(result_path_confusion)

# Printing report
report = classification_report(y_true=y, y_pred=model_predictions, output_dict=True)

df_report = pd.DataFrame(report).transpose()
df_confusion = pd.DataFrame(conf_matrix).transpose()

print(df_confusion)
print(df_report)

#######################################
# Writing results 
#######################################

import pandas as pd
writer = pd.ExcelWriter(file_to_save_results, engine='xlsxwriter')

df_empty1 = pd.DataFrame()
df_empty2 = pd.DataFrame()
df_empty3 = pd.DataFrame()


# Write data into excel sheets
df_report.to_excel(writer, sheet_name='Accuracy_Reports')
df_error.to_excel(writer, sheet_name='Errors')
# printing errors
#errored_predictions.to_excel(writer, sheet_name='Predictions_with_errors')
df_all_erros.to_excel(writer, sheet_name='Predictions_with_errors_details')
error_level_df.to_excel(writer, sheet_name='Predictions')
df_all_predictions.to_excel(writer, sheet_name='All Predictions')

# Save Accuracy figures in excel file
df_empty1.to_excel(writer, sheet_name='Accuracy_charts')
worksheet_acc = writer.sheets['Accuracy_charts']
worksheet_acc.insert_image('C2',result_path_accuracy)

# Save Error figures in excel file
df_empty2.to_excel(writer, sheet_name='Error_charts')
worksheet_err = writer.sheets['Error_charts']
worksheet_err.insert_image('C2',result_path_errors)


# Save Confusion figures in excel file
df_empty3.to_excel(writer, sheet_name='Confusion')
worksheet_con = writer.sheets['Confusion']
worksheet_con.insert_image('C2',result_path_confusion)


########################################################################################################################################
####################################################################
# What you need to show
####################################################################

#df_all_predictions .... dataframe that is of same lenght as input data
#df_confusion --- its a dataframe 
# df_report  ---its a dataframe
# ACCURACY --- its a value (e.g. 60)

############################################
# If there is any issue reading excel file, e.g. it is corrput etc; pls display this message and dont show any results

if (ERROR_READING == True):
  resultData = {
    "error": 'Failed! Cannot Read Data File; Pls check file'
  }
  print('Failed! Cannot Read Data File; Pls check file')
else:
  resultData = {
    "allPredictions": df_all_predictions.to_json(),
    "confusionMatrix": df_confusion.to_json(),
    "accuracy": str(ACCURACY),
    "reports": df_report.to_json(),
    "error": None
  }
  print(resultData)

######################################################################################################################################
#save file
writer.save()