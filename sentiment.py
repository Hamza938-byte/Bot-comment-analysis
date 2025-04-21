import re                  # Регулярные выражения
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

"""   Реализация анализа отзывов на тональность.   """


# Функция для очистки текста - удаление всех символов кроме цифр.
def clear_text(text):
    clear_text = re.sub(r'[^А-яЁё]+', ' ', str(text)).lower()
    return ' '.join(clear_text.split())


# Функция для удаление стоп слов
def clean_stop_words(text, stopwords):
    text = [word for word in text.split() if word not in stopwords]
    return ' '.join(text)


# Функция анализа тональности слов
def analysis(csvName):
    Nabor = pd.read_csv(csvName)['comment']  # Создание массива отзывов
    result = ''                              # Результат

    mostPositive = []                        # массив позитивных отзывов
    mostNegative = []                        # массив негативных отзывов

    # Проходим по каждому отзыву
    for i in range(len(Nabor)):
        # Очистка текста от стоп слов и спецсимволов, приведение к нижнему регистру и т.д.
        text = clean_stop_words(clear_text(Nabor[i]), stopwords)

        # Векторизация слов
        tf_idf_text = counter_idf.transform([text])
        # Предсказание - обученная модель логистической регрессии от 0 до 1
        toxic_proba = model_lr.predict_proba(tf_idf_text)

        # Разделение на позитивные/негативные отзывы
        # Формат строки: "Исходный текст -> Вероятность 0.XXXXX"
        if toxic_proba[0, 0] > toxic_proba[0, 1]:
            mostNegative.append\
            (f'{Nabor[i]} -> Вероятность негатива {toxic_proba[0, 0]:.5f}\n\n')

        else:
            mostPositive.append\
            (f'{Nabor[i]} -> Вероятность позитива {toxic_proba[0, 1]:.5f}\n\n')

    # Сортирует списки по вероятности (извлекает число из строки, например, 0.12345 из "0.12345\n\n").
    # Сортировка по убыванию
    mostPositive.sort(key=lambda x: float(x[-9:-2]), reverse=True)
    mostNegative.sort(key=lambda x: float(x[-9:-2]), reverse=True)

    # Формирование итогового результата
    result = ('📊 Анализ товара\n' + '✅ Позитивные отзывы:\n'
              + ''.join(mostPositive[:2])
              + '\n' + '❌ Негативные отзывы:\n'
              + ''.join(mostNegative[:2]))
    # Расчёт доли позитивных текстов
    ratioPos = len(mostPositive)/(len(mostPositive)+len(mostNegative))*100

    # Сообщение о выполненной работе
    print('done!')

    return f'{result}\n{ratioPos:.0f}% позитивных\n{100-ratioPos:.0f}% негативных'


# --------------------------------------------- #
#        Работа с тренировочным датасетом       #
# --------------------------------------------- #
stopwords = set(stopwords.words('russian'))
labeled_tweets = pd.read_csv('tweets/labeled_tweets_clean.csv', index_col=0).dropna()

# предварительно разделим выборку на тестовую и обучающую
train, test = train_test_split(labeled_tweets, test_size=0.2,
                               stratify=labeled_tweets['label'],
                               random_state=12348)

# инцициализируем векторайзер и укажем размер n-грамм
counter_idf = TfidfVectorizer(ngram_range=(1, 1))

# Получаем словарь и idf только из тренировочного набора данных
count_train = counter_idf.fit_transform(train['text_clear'])

# Применяем обученный векторайзер к тестовому набору данных
count_test = counter_idf.transform(test['text_clear'])

# Инициализируем модель с параметрами по умолчанию
# Далее эта модель(model_lr) будет использована для анализа
model_lr = LogisticRegression(random_state = 12345, max_iter = 10000, n_jobs = -1)

# Подбираем веса для слов с помощь fit на тренировочном наборе данных
model_lr.fit(count_train, train['label'])

# Получаем прогноз модели на тестовом наборе данных
predict_count_proba = model_lr.predict_proba(count_test)

# Сообщение о начале работы
print('started!')


