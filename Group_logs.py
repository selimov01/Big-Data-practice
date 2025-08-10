'''
У нас есть сервер с любимыми домашними питомцами, который отдаёт красивые картинки котиков, собачек и всего, что душе угодно. Обычному пользователю можно смотреть, публиковать или же удалять фото питомцев, другие действия/ручки/uri/hadlers ему недоступны.

Сервер обычно не сбоит, но иногда количество ошибок превышает норму, поэтому вам дали задание: собрать статистику по запросам про животных. Вам необходимо проанализировать логи и собрать следующую статистику по этим запросам пользователей:

1. сгруппировать запросы по коду ответа
2. для каждого уникального кода ответа определить минимальное, максимальное время ответа, а также 75 перцентиль от времени ответа
3. вывести % ошибочных запросов (будем считать ошибочными запросами все, у которых код ответа 5**)

Полезная ссылка про расчёт перцентилей: https://ru.stackoverflow.com/questions/1095777/Что-такое-перцентиль-как-с-ним-работать-и-как-его-вычислять

Формат вывода
На выходе ожидается несколько отформатированных чисел через пробел в формате:
<код ответа> <количество запросов c таким кодом> <минимальное время ответа> <максимальное время> <75 процентиль> 
<код ответа> <количество запросов c таким кодом> <минимальное время ответа> <максимальное время> <75 процентиль>
<процент ошибочных запросов>

ниже есть пример
все ответы необходимо округлить до целого числа (в меньшую сторону)

Пример

ВВОД
[2025-01-31 21:35:27.913140 MSD +000] GET t_id 0 /pet ?color=orange &test=True &id=31 HTTP/3.0 200 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 873ms
[2025-01-31 21:35:27.913140 MSK +000] DELETE t_id 1 /pet ?number=3 &id=25 HTTP/1.1 200 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 968ms
[2025-01-31 21:35:27.913140 SAMT +000] DELETE t_id 2 /pet ?number=1 &id=25 HTTP/1.1 409 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 364ms
[2025-01-31 21:35:27.913140 MSK +000] GET t_id 3 /status ?format=raw  HTTP/3.0 200 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 712ms
[2025-01-31 21:35:27.913140 MSD +000] POST t_id 4 /pet ?test=False &number=3 &color=gray &id=21 HTTP/3.0 409 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 426ms
[2025-01-31 21:35:27.913140 MSD +000] DELETE t_id 5 /pet ?test=False &id=29 HTTP/1.1 500 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 534ms
[2025-01-31 21:35:27.913140 MSD +000] DELETE t_id 6 /pet ?test=False &color=black &id=40 HTTP/3.0 200 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 419ms
[2025-01-31 21:35:27.913140 MSK +000] DELETE t_id 7 /pet ?color=orange &test=False &id=30 HTTP/3.0 409 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 463ms
[2025-01-31 21:35:27.913140 MSK +000] GET t_id 8 /status ?format=raw  HTTP/3.0 200 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 282ms
[2025-01-31 21:35:27.913140 MSD +000] GET t_id 9 /status ?format=plaintext  HTTP/2.0 409 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 597ms
[2025-01-31 21:35:27.913140 MSK +000] DELETE t_id 10 /pet ?color=black &number=1 &id=31 HTTP/1.1 409 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 106ms
[2025-01-31 21:35:27.913140 SAMT +000] POST t_id 11 /pet ?number=3 &test=True &color=black &id=40 HTTP/1.1 500 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 968ms
[2025-01-31 21:35:27.913140 MSD +000] DELETE t_id 12 /pet ?color=orange &test=False &id=35 HTTP/1.1 500 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 879ms
[2025-01-31 21:35:27.913140 MSK +000] DELETE t_id 13 /pet ?number=2 &test=False &color=orange &id=21 HTTP/2.0 200 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 288ms
[2025-01-31 21:35:27.913140 MSK +000] GET t_id 14 /status ?format=plaintext  HTTP/2.0 500 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 520ms
[2025-01-31 21:35:27.913140 SAMT +000] GET t_id 15 /status ?format=plaintext  HTTP/3.0 200 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 515ms
[2025-01-31 21:35:27.913140 SAMT +000] GET t_id 16 /status ?format=raw  HTTP/2.0 500 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 163ms
[2025-01-31 21:35:27.913140 MSK +000] GET t_id 17 /status ?format=pretty  HTTP/3.0 200 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0 642ms
[2025-01-31 21:35:27.913140 SAMT +000] DELETE t_id 18 /pet ?test=False &id=32 HTTP/1.1 200 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 864ms
[2025-01-31 21:35:27.913140 MSK +000] DELETE t_id 19 /pet ?test=True &id=21 HTTP/2.0 200 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0 97ms  

ВЫВОД
200 6 97 968 873
409 4 106 463 463
500 3 534 968 968
23
'''

filename = "input.txt"

data = {}
total = 0
errors = 0

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        if "/status" in line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        for i in range(len(parts)):
            if parts[i].startswith("HTTP/"):
                code = int(parts[i + 1])
                time_ms = int(parts[-1].replace("ms", ""))

                if code not in data:
                    data[code] = []
                data[code].append(time_ms)

                total += 1
                if 500 <= code <= 599:
                    errors += 1
                break

codes = sorted(data.keys())

for code in codes:
    times = data[code]
    times.sort()
    min_time = times[0]
    max_time = times[-1]
    idx = int(0.75 * len(times))
    if idx > 0:
        perc75 = times[idx - 1]
    else:
        perc75 = times[0]
    print(code, len(times), min_time, max_time, perc75)

print(errors * 100 // total)