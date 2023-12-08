# from keras.models import load_model
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# import numpy as np

# class SentimentAnalyzer:
#     def __init__(self, model_path):
#         self.model = load_model(model_path)
#         self.tokenizer = Tokenizer()

#     def tokenize_text(self, text):
#         sequences = self.tokenizer.texts_to_sequences([text])
#         padded_sequences = pad_sequences(sequences, maxlen=self.model.input_shape[1])
#         return padded_sequences

#     def analyze_sentiment(self, text):
#         tokenized_text = self.tokenize_text(text)
#         sentiment_score = self.model.predict(np.array(tokenized_text))[0][0]
#         print(sentiment_score)
#         return 'Positif' if sentiment_score > 0.5 else 'Negatif'