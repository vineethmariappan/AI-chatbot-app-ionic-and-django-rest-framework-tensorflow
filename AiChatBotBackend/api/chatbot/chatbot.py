import nltk
from nltk.stem.lancaster import  LancasterStemmer
stemmer = LancasterStemmer()
import  numpy
import tflearn
import  tensorflow
import random
import json
import pickle
import os

cwd = os.getcwd() 
with open(cwd+"\\api\\chatbot\\intents.json") as file:
    data = json.load(file)
try:
    with open(cwd+"\\api\\chatbot\\data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words=[]
    labels=[]
    docs_x=[]
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]: #tokenize -> get all words
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"]) # mapping each pattern with their tag

            if intent["tag"] not in labels:
                labels.append(intent["tag"]) #label stores all tags available

    words = [stemmer.stem(w.lower()) for w in words if w != "?"] #removes symbols and finds the root of words [ex what's -> what]
    words = sorted(list(set(words)))

    labels = sorted(labels)
    # will have bunch of 0s and 1 as lists
    training =[]
    output = []
    out_empty = [0 for _ in range(len(labels))]
    # mapping what words are present in every docs_x(pattern) using 1 (present output ) and 0 (not present)
    for x,doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc] #removes symbols and finds the root of words [ex what's -> what] doing the same process we did for the words

        for w in words:
            if w in wrds: # if word is present then add 1 else 0
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1 #mapping of bags to the corresponding labels

        training.append(bag) #x train
        output.append(output_row) #y train

    training = numpy.array(training)
    output = numpy.array(output)

    #saving the model data

    with open(cwd+"\\api\\chatbot\\data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()
#training the model starts here
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #softmax -> gives probabilty for resulting output layers
net = tflearn.regression(net)
model = tflearn.DNN(net)

try:
    model.load(cwd+"\\api\\chatbot\\model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True) #n_epoch no of times it sees the same data
    model.save(cwd+"\\api\\chatbot\\model.tflearn")
#training the model ends here

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w == se:
                bag[i]=1
    return numpy.array(bag)

def chat(inp):
    # print("works!")
    results = model.predict([bag_of_words(inp,words)])[0]
    results_index=numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index]<0.7:
        return "I didnt get that , try again"
    # else:
    for tg in data["intents"]:
        if tg["tag"] == tag:
            responses = tg['responses']
            break
    return random.choices(responses)[0]

