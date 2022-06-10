# For the neural network
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# For word processing
import nltk
import string
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Function to apply the preprocessing on given text
def transform_text(text):
    le = WordNetLemmatizer()
    tag_lis = ['JJ','JJR','JJS','RB','RBR','RBS','VB','VBG','VBD','VBN','VBP','VBZ']
    # tokenize + case lowering
    text = nltk.word_tokenize(text.lower())
    # pos tagging
    ps = nltk.pos_tag(text)
    y = list()
    text.clear()
    for x,z in ps:
       if z in tag_lis:
           y.append(x)
    text = y[:]
    y.clear()
    # isalpha checking 
    for i in text:
        if i.isalpha():
            # stopwords + punctuation removing + Lemmatization
            if i not in stopwords.words('english') and i not in string.punctuation:
                y.append(le.lemmatize(i,pos = 'v'))
    return " ".join(y)


# IMP variables for neural network
# IMP Variables
vocab_size = 50000
embedding_dim = 16
max_length = 150
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"

# Importing the model files
tokenizer = pickle.load(open(r'D:\Server\server_models\tokenizer.pkl', 'rb'))
model = tf.keras.models.load_model(r'D:\Server\server_models\ann.h5')

def predi(text):
    #text = transform_text(text)
    sentence = [text]
    sequences = tokenizer.texts_to_sequences(sentence)
    padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    result = model.predict(padded)
    res = round((result[0])[0],0)
    res = int(res)

    return res

def filePredict(rows):
	a=[]
	for row in rows:
		b=[]
		row=str(row)
		b.append(row)
		pred = predi(row)
		if(pred==1):
			b.append("'Truthful'")
		else:
			b.append("'Deceptive'")
		a.append(b)
	return a