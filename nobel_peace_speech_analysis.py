import pandas as pd
import nltk
import os
from nltk.tokenize import PunktSentenceTokenizer
from collections import Counter
from nltk.corpus import stopwords 

stop_words = set(stopwords.words('english'))
#initialize pandas Dataframe for later use
df = pd.DataFrame()

#define the path where the speech files are found
path = "C:\\Users\\eaesp\\OneDrive\\Desktop\\(Thick German Accent) Python -- Thorsten Altenkirch\\nobelspeeches"
nobel_speeches = os.listdir(path)

files = sorted([os.path.join(path, file) for file in nobel_speeches if file.endswith('.txt')])

#create a function that will open the file read it, making the text available in python
def read_file(file_name):
  #open the file with the correct encoding and save it to a variable "file"
  with open(file_name, 'r+', encoding='utf-8') as file:
    #read the file and save it to a variable "file_text"
    file_text = file.read()
   #return the text for use outside of the function 
  return file_text

#call the read_file function for all of the documents in the folder
speeches = [read_file(doc) for doc in files]

#create a function that will process the data
def process_speeches(speeches):
  #create a new list to append the cleaned data to
  word_tokenized_speeches = list()
  #loop through each speech in the argument
  for speech in speeches:
    #initialize the sentence Tokenizer
    sentence_tokenizer = PunktSentenceTokenizer()
    #apply the sentence tokenizer to the speech
    sentence_tokenized_speech = sentence_tokenizer.tokenize(speech)
    #create a new list to append the tokenized sentences too
    word_tokenized_sentences = list()
    #loop through each sentence in the tokenized speech
    for sentence in sentence_tokenized_speech:
      #strip each sentence of punctuation and split them into words
      word_tokenized_sentence = [word.lower().strip('.').strip('?').strip('!') for word in sentence.replace(",","").replace("-"," ").replace(":","").split()]
      #append the stripped sentences to the new list
      word_tokenized_sentences.append(word_tokenized_sentence)
    #append the cleaned sentences to the original list
    word_tokenized_speeches.append(word_tokenized_sentences)
  #return the original list for us outside of the function
  return word_tokenized_speeches

processed_text = process_speeches(speeches)
#print to make sure the function works (can be commented out)
#print(processed_text)

#define a function that will merge all of the speeches together into one pool
def merge_speeches(speeches):
  #create an empty list to append the sentences too
  all_sentences = list()
  #loop through each speech in the processed text
  for speech in speeches:
    #loop through each sentence in the speech
    for sentence in speech:
      #append each sentence to the new list
      all_sentences.append(sentence)
  #return the list
  return all_sentences

#call the function and print it to make sure it works (can be commented out)
merged_speeches = merge_speeches(processed_text)
#print(merged_speeches)

#create a function that will find each individual speakers sentences for analysis
def get_speaker_sentences(speaker):
  #this list comprehension concatenates both the path and the file, joining them together to access the files individually if such a file exists in the folder
  files = sorted([os.path.join(path, file) for file in nobel_speeches if speaker.lower() in file.lower()])
  #the speeches variable holds a list comprehension that uses the earlier read_file function to read the individual file as referenced by the speaker name
  speeches = [read_file(file) for file in files]
  #uses th earlier function process speech to tokenize the sentences and words while removing punctuation
  processed_speeches = process_speeches(speeches)
  #uses the earlier merge_speeches function to create a list of all of the sentences in the speech
  all_sentences = merge_speeches(processed_speeches)
  #returns the sentences for use outside of the function
  return all_sentences

#call the function and print it to check if it works (can be commented out)
speaker_sentences = get_speaker_sentences("mother_theresa")
#print(speaker_sentences)

#create a function that will allow a user to look for most common words among more than one nobel lecturer
def get_speakers_sentences(speakers):
  #create a new list that we can append tokenized sentences to
  all_sentences = list()
  #loop through each speaker within speakers
  for speaker in speakers:
    #this list comprehension concatenates both the path and the file, joining them together to access the files individually if such a file exists in the folder
    files = sorted([os.path.join(path, file) for file in nobel_speeches if speaker in file])
    #the speeches variable holds a list comprehension that uses the earlier read_file function to read the individual file as referenced by the speaker name
    speeches = [read_file(file) for file in files]
    #uses th earlier function process speech to tokenize the sentences and words while removing punctuation
    processed_speeches = process_speeches(speeches)
    #uses the earlier merge_speeches function to create a list of all of the sentences in the speech
    all_speaker_sentences = merge_speeches(processed_speeches)
    #extend the new list with the list created from the merge_speeches function
    all_sentences.extend(all_speaker_sentences)
  #return the list of all_sentences for use outside of the function
  return all_sentences

#create a function that can find all of the most frequently used words by speaker(s)
def most_frequent_words(list_of_sentences):
  #list comprehension finds all of the words in the sentences provided
  all_words = [word for sentence in list_of_sentences for word in sentence]
  #Counter attribute .most_common() is able to parse through all of the words and find the most common as well as their tally
  return Counter(all_words).most_common()

#call the get_speaker_sentences or get_speakers_sentences function 
speakers_sentences = get_speakers_sentences(["barack_obama", "mother_theresa", "dalai_lama", "martin_luther_king"])
#print(speakers_sentences)

#call the function and print it to make sure it works (can be commented out)
speakers_freq_words = most_frequent_words(speakers_sentences)
#print(speakers_freq_words)