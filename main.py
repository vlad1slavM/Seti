#!/usr/bin/env python3
import requests
import re


class Regulars:
    link = re.compile(r'<code>/(.+?)</code>|<a href=\"/(.+?)\"')
    task = re.compile(r'POST|GET|Загрузите|Перейдите')
    keys = re.compile(r'<code>(.+?)</code>')
    cookie = re.compile(r'cookie(.+?)</table>')
    header = re.compile(r'заголовки(.+?)</table>')
    data = re.compile('формы(.+?)</table>')
    params = re.compile(
        r'параметры запроса, указанные в таблице:(.+?)</table>')
    number = re.compile(r'Шаг #(.+?)')
    link_go_over = re.compile(r"href=['\"](.+?)['\"]>")


class GetPost:
    def __init__(self):
        self.data = {}
        self.task = []
        self.link = []
        self.dict_cookie = {}
        self.dict_header = {}
        self.dict_data = {}
        self.dict_params = {}
        self.link_go_over = []

    @staticmethod
    def parser(text, keyword):
        result = {}
        raw_cookie = re.findall(rf"{keyword}(.+?)</table>", text, re.DOTALL)
        if not raw_cookie:
            return None
        else:
            head_list = Regulars.keys.findall(raw_cookie[0])
            for i in range(0, len(head_list) - 1, 2):
                result[head_list[i]] = head_list[i + 1]
        return result

    def parser_cookie(self, text):
        result = {'user': '4a0c8246d4578d06fd5aa2dac540e7e4'}
        raw_cookie = re.findall(r"cookie:(.+?)</table>", text, re.DOTALL)
        if not raw_cookie:
            return result
        else:
            head_list = re.findall(r"<code>(.+?)</code>", raw_cookie[0])
            for i in range(0, len(head_list) - 1, 2):
                req = re.compile('[а-яА-Я]]')
                cookie = req.sub('', head_list[i + 1])
                result[head_list[i]] = cookie
        return result

    def get_data(self, url):
        data = {}
        cookies = {'user': '4a0c8246d4578d06fd5aa2dac540e7e4'}
        r = requests.get(url, cookies=cookies)

        with open('site.txt', 'a', encoding='UTF-8') as file:
            file.write(r.text)
        task_local = re.findall(Regulars.task, r.text)
        link_local = re.findall(Regulars.link, r.text)
        keys_local = re.findall(Regulars.keys, r.text)
        link_go_over_local = re.findall(Regulars.link_go_over, r.text)
        if len(keys_local) != 0:
            if keys_local[0][0] == '/':
                keys_local = keys_local[1:]
        for i in range(0, len(keys_local) - 1):
            if i % 2 == 1:
                continue
            else:
                data[keys_local[i]] = keys_local[i + 1]
        self.data = data
        self.task = task_local
        self.link = link_local
        self.link_go_over = link_go_over_local
        self.dict_cookie = GetPost.parser_cookie(self, r.text)
        self.dict_data = GetPost.parser(r.text, "формы")
        self.dict_header = GetPost.parser(r.text, 'заголовки')
        self.dict_params = GetPost.parser(r.text, "параметры")
        GetPost.decide_task(self)

    def decide_task(self):
        if self.task[0] == "GET":
            print("get")
            GetPost.get_request(self)
        elif self.task[0] == "POST":
            print('post')
            GetPost.post_request(self)
        elif self.task[0] == "Перейдите":
            print("Перейдите")
            GetPost.go_over_request(self)

    def post_request(self):
        if self.link[0][0] == '':
            url = 'http://hw1.alexbers.com/' + str(self.link[0][1])
        else:
            url = 'http://hw1.alexbers.com/' + str(self.link[0][0])
        s = requests.post(url, data=self.dict_data, cookies=self.dict_cookie,
                          params=self.dict_params, headers=self.dict_header)
        print(url)
        print(re.findall(Regulars.number, s.text))
        print(str(self.dict_data) + '\n' + str(self.dict_cookie) + '\n' + str(
            self.dict_params) + '\n' + str(self.dict_header))
        GetPost().get_data(url)

    def get_request(self):
        if self.link[0][0] == '':
            url = 'http://hw1.alexbers.com/' + str(self.link[0][1])
        else:
            url = 'http://hw1.alexbers.com/' + str(self.link[0][0])
        s = requests.get(url, data=self.dict_data, cookies=self.dict_cookie,
                         params=self.dict_params, headers=self.dict_header)
        print(url)
        print(str(self.dict_data) + '\n' + str(self.dict_cookie) + '\n' + str(
            self.dict_params) + '\n' + str(self.dict_header))
        print(re.findall(Regulars.number, s.text))
        GetPost().get_data(url)

    def go_over_request(self):
        url = 'http://hw1.alexbers.com' + str(self.link_go_over[0])
        s = requests.get(url, data=self.dict_data, cookies=self.dict_cookie,
                         params=self.dict_params, headers=self.dict_header)
        print(url)
        print(str(self.dict_data) + '\n' + str(self.dict_cookie) + '\n' + str(
            self.dict_params) + '\n' + str(self.dict_header))
        print(re.findall(Regulars.number, s.text))
        GetPost().get_data(url)



if __name__ == '__main__':
    GetPost().get_data('http://hw1.alexbers.com/')
