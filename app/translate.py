import os
import json
import requests


# Конфигурационные данные
# Путь к файлу, который содержит токен Yandex Cloud
token_path = 'IAM_token.token'
# Идентификатор каталога
folder_id = 'b1gbkod773b3hen8brto'

# Подгрузка токена путем считывания данных из файла
IAM_TOKEN = os.path.join(os.getcwd(), token_path)
with open(IAM_TOKEN) as f:
    IAM_TOKEN = f.read().strip()


def translate(text: str, target_language: str) -> str:
    '''Функция для перевода текста на выбранный язык.

    Аргументы:
        text (string) - текст, который необходимо перевести.
        target_language (string) - язык, на который необходимо перевести.
            Например, "en" - для перевода на английский.
    '''

    # Т.к. переводчик переводит не текст, а токены (текст разделенный на слова)
    # необходимо исходный текст разделить по символу "пробел"
    texts = text.split(' ')
    # Задаем параметры, которые будут отправлены в теле запроса
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }
    # Формируем данные для заголовка запроса
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }
    # Получаем ответ в виде текста, имеющего структуру json
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                            json=body,
                            headers=headers
                            )
    print(response)
    # Конвертируем полученный результат в json
    response_json = json.loads(response.text)
    # Создаем переменную для хранения переведенного текста,
    # который будет отправлен пользователю
    text_for_send = ''
    # Считываем каждый токен из ответа и формируем конечный результат
    for token in response_json['translations']:
        # Т.к. токены - это набор слов с знаками,
        # то для получения читаемого текста необходимо 
        # добавить пробел между каждым из токенов
        text_for_send += token['text'] + ' '
    # Удаляем пробелы, находящиеся в начале и конце текста
    text_for_send = text_for_send.strip()
    # Отправляем пользователю переведенный текст
    return text_for_send
