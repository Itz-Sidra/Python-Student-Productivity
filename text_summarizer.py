import spacy
import spacy.cli
spacy.cli.download("en_core_web_sm")
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """In the formidable years, this had no specific theme planned. The main aim was to promote and advocate the public on important issues. Also, in the first three years, one of the central activities done to help the day become special was the 2-hour telecast by the US information agency satellite system. 

Mental health is not just a concept that refers to an individual’s psychological and emotional well being. Rather it’s a state of psychological and emotional well being where an individual is able to use their cognitive and emotional capabilities, meet the ordinary demand and functions in the society. According to WHO, there is no single ‘official’ definition of mental health.

Thus, there are many factors like cultural differences, competing professional theories, and subjective assessments that affect how mental health is defined. Also, there are many experts that agree that mental illness and mental health are not antonyms. So, in other words, when the recognized mental disorder is absent, it is not necessarily a sign of mental health. 

One way to think about mental health is to look at how effectively and successfully does a person acts. So, there are factors such as feeling competent, capable, able to handle the normal stress levels, maintaining satisfying relationships and also leading an independent life. Also, this includes recovering from difficult situations and being able to bounce back.  """

def summarizer(rawdocs):
    stopwords= list(STOP_WORDS)
    #print(stopwords)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)

    tokens = [token.text for token in doc]
    #print(tokens)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    #print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)

    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len)

    summary = nlargest(select_len, sent_scores, key = sent_scores.get )
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    #print(text)
    #print(summary)
    #print("Length of original text: ",len(text.split(' ')))
    #print("Length of summary text: ",len(summary.split(' ')))
    
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))
