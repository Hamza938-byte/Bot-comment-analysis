import re

import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# Регулярные выражения

def clear_text(text):
    clear_text = re.sub(r'[^А-яЁё]+',' ',str(text)).lower() # Удаляет все некириллические символы, заменяя их на ' '
    
    return ' '.join(clear_text.split())

def clean_stop_words(text, stopwords):
    text = [word for word in text.split() if word not in stopwords]

    return ' '.join(text)

def analysis(csvName):
    Nabor = pd.read_csv(csvName)['textOriginal']
    result = ''
    mostPositive = []
    mostNegative = []

    for i in range(len(Nabor)):   

        text = clean_stop_words(clear_text(Nabor[i]),stopwords)
        tf_idf_text = counter_idf.transform([text])
        toxic_proba = model_lr.predict_proba(tf_idf_text)

        if toxic_proba[0,0]>toxic_proba[0,1]:
            mostNegative.append\
            (f'{Nabor[i]} -> Вероятность негатива {toxic_proba[0,0]:.5f}\n\n')

        else:
            mostPositive.append\
            (f'{Nabor[i]} -> Вероятность позитива {toxic_proba[0,1]:.5f}\n\n')

    mostPositive.sort(key=lambda x: float(x[-9:-2]),reverse=True)
    mostNegative.sort(key=lambda x: float(x[-9:-2]),reverse=True)
    result = 'Наиболее позитивные:\n'+''.join(mostPositive[:3])+'\n'+'Наиболее негативные:\n'+''.join(mostNegative[:3])
    ratioPos = len(mostPositive)/(len(mostPositive)+len(mostNegative))*100
    print('done!')

    return f'{result}\n{ratioPos:.0f}% позитивных\n{100-ratioPos:.0f}% негативных'

# --------------------------------------------- #

stopwords = set(stopwords.words('russian'))

labeled_tweets = pd.read_csv('tweets/labeled_tweets_clean.csv', index_col=0).dropna()

# предварительно разделим выборку на тестовую и обучающую
train, test = train_test_split(labeled_tweets,test_size = 0.2,stratify = labeled_tweets['label'],random_state = 12348)

# инцициализируем векторайзер и укажем размер n-грамм
counter_idf = TfidfVectorizer(ngram_range=(1,1))

# Получаем словарь и idf только из тренировочного набора данных
count_train = counter_idf.fit_transform(train['text_clear'])

# Применяем обученный векторайзер к тестовому набору данных
count_test = counter_idf.transform(test['text_clear'])

# Инициализируем модель с параметрами по умолчанию
model_lr = LogisticRegression(random_state = 12345,
                                    max_iter = 10000,
                                    n_jobs = -1)

# Подбираем веса для слов с помощь fit на тренировочном наборе данных
model_lr.fit(count_train, train['label'])

# Получаем прогноз модели на тестовом наборе данных
predict_count_proba = model_lr.predict_proba(count_test)

print('started!')


