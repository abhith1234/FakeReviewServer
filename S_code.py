#Importing required library
import pickle
# import pandas as pd
#for word processing
from helperfunctions import transform_text, predi
# Function to simplify the predictions of models
def resolver(result,inv=False):
  if inv==True:
    if result[0]==0:
      return False
    elif result[0]==1:
      return True

  
  if result[0]==0:
    return True
  elif result[0]==1:
    return False

def predictor(istr):

  text = transform_text(istr)

  predictions_NN = predi(text)

  rNN = resolver([predictions_NN],inv=True)

  return [rNN]