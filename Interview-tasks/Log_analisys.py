'''
В вашем сервисе есть веб-сервер, который раздаёт полезные данные пользователям. Один из менеджеров сервиса считает, что вашими данными пользуются всё больше и больше людей из мобильных браузеров, и поэтому нужно сфокусироваться на том, чтобы сделать мобильную вёрстку. Для того, чтобы проверить эту гипотезу, он попросил вас построить график процентного соотношения мобильных запросов ко всем запросам.

Для решения задачи у вас не нашлось времени, но время оказалось у вашего стажёра, который написал программу, размечающую лог запросов словами mobile / desktop / unknown. К сожалению, когда вы добрались проверить эту программу, стажёр был в отпуске, а график нужно уже строить. Программа выглядит рабочей, но есть несколько нюансов:

- она работает не очень быстро;
- она иногда потребляет много памяти;
- иногда она работает не совсем корректно.

Ниже приложен код программы. Ваша задача:
1. Найти и исправить логическую ошибку в коде;
2. Ускорить работу программы;
3. Уменьшить потребляемую память.
Если программа выдаёт неправильные значения, то оптимизировать её рано.

--------------------------------------------

import sys
from typing import List


class LogMobileDistinguisher:
    def __init__(self, desktop_file_name, mobile_file_name):
        self.desktop = self.read_file(desktop_file_name)
        self.mobile = self.read_file(mobile_file_name)
        self.process_log()

    @staticmethod
    def read_file(file_name: str) -> List[str]:
        with open(file_name, 'r') as fi:
            result = []
            for line in fi.readlines():
                result.append(line.strip())
            return result

    def get_line_client(self, line_ua: str) -> str:
        result = 'unknown'

        for ua in self.desktop:
            if ua == line_ua:
                result = 'desktop'

        for ua in self.mobile:
            if ua == line_ua:
                result = 'mobile'

        return result

    @staticmethod
    def get_line_fields(line: str) -> List[str]:
        result = []
        in_string = False
        s = ''
        for field in line.strip().split(' '):
            if not in_string:
                if field.startswith('"') and not field.endswith('"'):
                    in_string = True
                    s = field[1:]
                else:
                    result.append(field)
            else:
                if field.endswith('"'):
                    s += ' ' + field[:-1]
                    result.append(s)
                    in_string = False
                else:
                    s += ' ' + field
        return result

    def process_log(self):
        for line in sys.stdin.readlines():
            fields = self.get_line_fields(line)
            client = self.get_line_client(fields[6])
            print(client + ' ' + line.strip())


if __name__ == '__main__':
    LogMobileDistinguisher('d.txt', 'm.txt')

--------------------------------------------

Пример строк лога, которые подаются на вход программе:
2001:db8:9a88:ac14:3689:9a62:872d:e784 [25/03/2024:12:42:54 +0300] "GET /how-much-is-the-fish HTTP/1.0" 301 58940 "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
2001:db8:4a37:82d9:d8f7:ab69:a024:8cf1 [25/03/2024:12:42:55 +0300] "GET /penguins-jump-in-the-air HTTP/1.0" 500 66486 "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
2001:db8:4f6e:aa51:a90d:62d6:95e5:d50 [25/03/2024:12:42:55 +0300] "GET /this-is-a-lucky-string HTTP/1.0" 200 46842 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0"

Пример ожидаемого размеченного лога:
desktop 2001:db8:9a88:ac14:3689:9a62:872d:e784 [25/03/2024:12:42:54 +0300] "GET /how-much-is-the-fish HTTP/1.0" 301 58940 "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
mobile 2001:db8:4a37:82d9:d8f7:ab69:a024:8cf1 [25/03/2024:12:42:55 +0300] "GET /penguins-jump-in-the-air HTTP/1.0" 500 66486 "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
desktop 2001:db8:4f6e:aa51:a90d:62d6:95e5:d50 [25/03/2024:12:42:55 +0300] "GET /this-is-a-lucky-string HTTP/1.0" 200 46842 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0"

Стажёр собрал известные агенты десктопных и мобильных браузеров в файликах d.txt и m.txt соответственно. Приведём примеры строк из этих файлов (в реальных тестах строк, разумеется, больше).

d.txt:
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:59.0) Gecko/20100101 Firefox/59.0

m.txt:
Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36

Если агента в файлах нет, нужно выводить unknown, дополнительные эвристики про мобильность агента придумывать не нужно.

'''

import sys

class LogMobileDistinguisher:
    def __init__(self, desktop_file_name, mobile_file_name):
        self.desktop = self.read_file(desktop_file_name)
        self.mobile = self.read_file(mobile_file_name)
        self.ua_cache = {}
        self.process_log()

    @staticmethod
    def read_file(file_name: str) -> set[str]:
        with open(file_name, 'r') as f:
            return set(line.strip() for line in f)

    def get_line_client(self, ua: str) -> str:
        
        if ua in self.ua_cache:
            return self.ua_cache[ua]

        if ua in self.desktop:
            self.ua_cache[ua] = 'desktop'
        elif ua in self.mobile:
            self.ua_cache[ua] = 'mobile'
        else:
            self.ua_cache[ua] = 'unknown'
        return self.ua_cache[ua]

    @staticmethod
    def extract_user_agent(line: str) -> str:
        start = line.rfind('"')
        if start == -1:
            return ''

        end = line.rfind('"', 0, start)
        if end == -1:
            return ''
        return line[end+1:start]

    def process_log(self):
        for line in sys.stdin:
            line = line.rstrip('\n')
            ua = self.extract_user_agent(line)
            client = self.get_line_client(ua)
            print(client, line)

if __name__ == '__main__':
    LogMobileDistinguisher('d.txt', 'm.txt')