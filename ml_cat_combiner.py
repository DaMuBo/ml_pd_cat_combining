import sys
import os
import pandas as pd
import numpy as np
import logging
import pickle

from pandas.api.types import is_string_dtype

class ml_combining():
    """
    A preprocessing Class which is building an information about the masking of categorical values based on a threshold in the training data ->
    unseen data will also be masked.
    
    Goal: reduce the number of attributes in a feature -> rare categories will be mapped to one category
    
    Methods:
    ----------------
        __init__(): Initalizes the class and the input parameters

        fit():

        transform():

        save_model():

        load_model()
    
    """
    def __init__(self, df=None,columns=None,threshold=0.01,unseen_data="map",placeholder='Other'):
        """
        Initiale Parameter zuweisen. 
        Inputs:
        ------------
        df: DataFrame,
            enthält das df auf das die Funktion angewendet werden soll
        columns: list
            enthält eine Liste an columns die entsprechend gemappt werden soll -> wenn keine Liste übergeben wird, werden alle nicht numerischen Columns automatisch gemappt
        threshold: float
            enthält die Anteilsgrenze [Wertebereich 0;1] unterhalb derer die Daten zusammengefasst werden sollen
        unseen_data: String
            enthält die strategie wie mit unbekannten Daten bei transform umgegangen werden soll.
                map = mappe alle unbekannten daten in die zusammenfassung
                ignore = ignoriere diese Werte und gib die original werte zurück
                unseen = erzeuge eine eigene kategorie unseen für diese unbekannten daten
        """
        self.df = df
        self.columns = columns
        self.threshold = threshold
        self.unseen_data = unseen_data
        self.mask = {}
        self.placeholder = placeholder
        
        
        
        
    def fit(self, df=None, columns=None,threshold=0.01,unseen_data="map", placeholder = 'Other'):
        """
        fitting new data to the model and train it
        """
        if df is not None:
            self.df = df.copy()
        if columns is not None:
            self.columns = columns
        else:
            self.columns = self.df.columns
        if threshold is not None:
            self.threshold = threshold
        if unseen_data is not None:
            self.unseen_data = unseen_data
        if placeholder != 'Other':
            self.placeholder = placeholder
    
        for c in self.columns:
            if is_string_dtype(self.df[c]):
                series = pd.value_counts(self.df[c])
                mask = (series/series.sum()).lt(self.threshold)
                self.mask[c] = mask
                self.df[c] =  np.where(self.df[c].isin(series[self.mask[c]].index),self.placeholder,self.df[c].values)
        return self
        
        
        
        
    def transform(self, df):
        """
        transforming the learned model on the new dataframe and returning the masked data
        """
        for c in df.columns:
            if c in self.mask.keys():
                if self.unseen_data =="map":
                    df[c] = np.where((df[c].isin(self.mask[c].index) == False) & (df[c].isnull() == False ),self.placeholder,df[c])
                    df[c] = np.where(df[c].isin(self.mask[c][self.mask[c] == True].index),self.placeholder,df[c])
                elif self.unseen_data == "ignore":
                    df[c] = np.where(df[c].isin(self.mask[c][self.mask[c] == True].index),self.placeholder,df[c])
                elif self.unseen_data == "unseen":
                    df[c] = np.where((df[c].isin(self.mask[c].index) == False) & (df[c].isnull() == False ),'Unknown',df[c])
                    df[c] = np.where(df[c].isin(self.mask[c][self.mask[c] == True].index),self.placeholder,df[c])
                    
                else:
                    logging.warning("""No valid strategy for unseen data defined. See docs for valid Variables""")
                
        return df
        
        
        
        
    def save_model(self,filename):
        """
        speichert die gelernte Struktur in einem File ab für die weitere Verwendung in einem 
        Produktivem Umfeld
        """
        output = {
            'columns':self.columns
            , 'mask':self.mask
            , 'unseen_data':self.unseen_data
            , 'placeholder':self.placeholder
        }
        pickle.dump(output, open(filename, 'wb'))
        
        
        
        
    def load_model(self, link):
        """
        lädt eine Struktur in das Objekt und gibt dieses danach zurück
        """
        inputi = pickle.load(open(link, 'rb'))
        self.columns = inputi['columns']
        self.mask = inputi['mask']
        self.unseen_data = inputi['unseen_data']
        self.placeholder = inpute['placeholder']
        
        return self