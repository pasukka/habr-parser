# Программа для парсинга Habr

✔ Python

✔  Requests

✔  BeautifulSoup

✔  Numpy

✔ Компьютерная лингвистика

## Описание задачи
Для составления корпуса текстов была написана программа для парсинга сайта habr.com, содержащего статьи разнообразных направлений, связанных с программированием.
Список хабов интересующих статей, относящихся к компьютерной лингвистике:
1.   Natural Language Processing;
2.   Artificial Intelligence;
3.   Искусственный интеллект';
4.   Data Mining + (Machine learning / Машинное обучение);
5.   Big Data + (Machine learning / Машинное обучение / Семантика);
6.   Поисковые технологии + (Data Mining / Machine learning / Машинное обучение / Big Data).

Были выбраны статьи, находящиеся во временном отрезке с 1 января 2010 года по 8 октября 2022 для получения достаточно представительного корпуса.

Страницы с новыми статьями добавляются на сайт последовательно по адресу https://habrahabr.ru/post/ и идентифицируются по номеру.

## Описание работы программы

На вход программе подается номер страницы. На следующем этапе происходит сравнение хабов со страницы с ключевыми хабами из составленного списка. Если статья удовлетворяет условию, то она сохраняется в формате html в указанную папку.

## Original file is located at
    https://colab.research.google.com/drive/13S76mhPxaaNy_IgnJU--CnQRgW6n5Ueo