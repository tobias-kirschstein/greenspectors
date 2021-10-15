from nltk import tokenize
from operator import itemgetter
import math

# Read input file, note the encoding is specified here
# It may be different in your text file
file = open('Amazon.txt', encoding="utf8")
dataset= file.read()

# set stop words
stop_words = set({'the','and','by','of','to','for','over','as','As','with','$1','100%','billion','$2'})


# split data
total_words = dataset.split()
# total word
total_word_length = len(total_words)
#print(total_word_length)
# total sentence
total_sentences = tokenize.sent_tokenize(dataset)
total_sent_len = len(total_sentences)
#print(total_sent_len)
# calculate tf scores
tf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in tf_score:
            tf_score[each_word] += 1
        else:
            tf_score[each_word] = 1


def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences]
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))


# calculate idf
idf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in idf_score:
            idf_score[each_word] = check_sent(each_word, total_sentences)
        else:
            idf_score[each_word] = 1

# Performing a log and divide
idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

#print(idf_score)

# calculate tf-idf
tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
#print(tf_idf_score)


# get n most important data
def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n])
    return result


# print 5 most important one
keywords2save = get_top_n(tf_idf_score, 5)
print(keywords2save)

with open('important_keywords.txt', 'w') as f:
    f.write('\n'.join(keywords2save))

# Close the file
file.close()
