import datetime
import glob
import pandas as pd

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

txt_files = glob.glob("txt_report/*.txt")
text_titles = [Path(text).stem for text in txt_files]

# Companies like to mention their own names A LOT, remove that
custom_stop_words = ENGLISH_STOP_WORDS.union([t.lower() for t in text_titles])
# Also years, when they did something
year = datetime.datetime.today().year
custom_stop_words = custom_stop_words.union([str(y) for y in range(year, year - 20, -1)])

# Catch-all stop list for the rest
custom_stop_words = custom_stop_words.union(['general', 'motors', 'mcdonald', 'disney', 'restaurants', 'j', 's'])
# 'palm', 'fuel', 'oil' <-- these actually seem kinda relevant for the sustainability stuff


bigram_vectorizer = TfidfVectorizer(input='filename', lowercase=True,
    stop_words=custom_stop_words, ngram_range=(1, 4), token_pattern=r'\b\w+\b', min_df=1)

tfidf_vector = bigram_vectorizer.fit_transform(txt_files)

tfidf_df = pd.DataFrame(tfidf_vector.toarray(), index=text_titles,
                        columns=bigram_vectorizer.get_feature_names())
# tfidf_df.loc['Document_Frequency'] = (tfidf_df > 0).sum()

tfidf_df = tfidf_df.stack().reset_index()
tfidf_df = tfidf_df.rename(columns={0:'tfidf', 'level_0': 'document','level_1': 'term', 'level_2': 'term'})
top_10_terms_per_doc = tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False]).groupby(['document']).head(10)
top_10_terms_per_doc.to_csv('TF-IDF/top_10_terms_per_doc_v2.csv', index=False)

top_10_terms = tfidf_df.sort_values(by=['tfidf'], ascending=[False]).head(10)
print(top_10_terms)
top_10_terms.to_csv('TF-IDF/top10_terms_v2.csv', index=False)

# print(tfidf_df)

# print(document_term_matrix.toarray())
# print(bigram_vectorizer.inverse_transform(document_term_matrix))

# transformer = TfidfTransformer(smooth_idf=False)
# tfidf = transformer.fit_transform(document_term_matrix.toarray())
# print(tfidf)
