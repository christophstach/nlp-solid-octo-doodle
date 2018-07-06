from tqdm import tqdm

import helpers as helper
from TextProcessing import lemmatize_word, stopwords


class NounChunkPreprocessor:
    """
    This preprocessor splits the texts into noun chunks
    which should represent the most important words of a text
    """

    def __init__(self, nlp, use_tqdm=True):
        self.nlp = nlp
        self.use_tqdm = use_tqdm

    def preprocess(self, articles):
        documents = []
        iterator = tqdm(articles, desc='Preprocessing articles') if self.use_tqdm else articles

        for article in iterator:
            documents.append(self.preprocess_article(article))

        return documents

    def preprocess_article(self, article):
        p_article = article.copy()
        p_article['text'] = self.preprocess_text(article['text'])

        return p_article

    def preprocess_text(self, text):
        use_own_stopwords = False
        text = helper.clean(text)  # Clean text and remove double spacy and special chars and copyrights.
        doc = self.nlp(text)

        sentences = []
        for sentence in doc.sents:  # Split text into sentences
            chunks = []

            for chunk in sentence.noun_chunks:  # Get noun_chunks out of sentence
                if use_own_stopwords:  # Remove stopwords
                    tokens = chunk.text.lower().split(' ')
                    tokens = list(filter(lambda token: token not in stopwords, tokens))
                else:
                    # chunk = self.nlp(chunk.text.lower())
                    # tokens = [token.text for token in chunk if not token.is_stop]
                    tokens = chunk.text.lower().split(' ')  # This method is way faster for checking for stopwords
                    tokens = list(filter(lambda token: not self.nlp.vocab[token].is_stop, tokens))

                tokens = list(filter(lambda token: token != '', tokens))
                tokens = list(map(lambda token: lemmatize_word(token), tokens))  # Lemmatize

                chunk = ' '.join(tokens)
                chunk = chunk.lower()  # lower all the text

                if chunk != '':
                    chunks.append(chunk)

            if len(chunks) > 0:  # Only append non empty tokens
                sentences.append(chunks)

        return helper.flatten(sentences)  # Merge words of the sentences together to a document array
