# -*- coding: utf-8 -*-
# @Time : 2023/1/16 8:04
# @Author : Installation
# @Email : 599575461@qq.com
# @File : tools.py
# @Project : Password_management_system
import argparse
import os
import uuid
from base64 import b64encode, b64decode, b16encode
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, ALL_COMPLETED
from typing import Union
from English.stardict import DictCsv
from Crypto.Cipher import AES
from requests import get


class English:

    def __init__(self, save_path: str, English_dict: str):
        self.csv = None
        self.all_task = list()
        self.len_ = int()

        self.save_path = save_path
        self.English_dict = English_dict

    def start(self):
        self.csv = DictCsv(self.English_dict)

    def paragraph_info(self, i):
        response = get(
            f"https://tts.youdao.com/fanyivoice?word={i}&le=eng&keyfrom=speaker-target"
        ).content
        with open(self.save_path + i + ".mp3", 'wb') as code:
            code.write(response)

    def main(self, text=None, type_=None, is_words_alpha=False):
        self.len_ = len(text)
        for a in os.listdir(self.save_path):
            if os.path.splitext(a)[1] == '.mp3':
                os.unlink(self.save_path + a)

        if is_words_alpha:
            with open("words_alpha.txt", 'r') as f:
                text = f.read().splitlines()[0:100]

        if type_ == 'list':
            wait([
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.paragraph_info, m) for m in text
            ],
                return_when=ALL_COMPLETED)
        else:
            wait([
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.paragraph_info, text)
            ],
                return_when=ALL_COMPLETED)

    def word_dispose(self, word):
        word = self.csv.query(word)
        if word['exchange'] == '':
            return [
                word['sw'], word['phonetic'], word['definition'],
                word['translation']
            ]
        else:
            return [
                word['sw'], word['phonetic'], word['definition'],
                word['translation'],
                {
                    i[0]: i[1]
                    for i in [i.split(":") for i in [i for i in word['exchange'].split("/")]
                              ]
                }
            ]

    def main_idea(self, words):
        self.len_ = len(words)
        data = list()
        if isinstance(words, str):
            self.all_task = [
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.word_dispose, words)
            ]
            self.main(is_words_alpha=False, text=words, type_='str')
        if isinstance(words, list):
            self.all_task = [
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.word_dispose, i) for i in words
            ]
            self.main(is_words_alpha=False, text=words)
        wait(self.all_task, return_when=ALL_COMPLETED)
        for future in as_completed(self.all_task):
            data.append(future.result())
        return data


class EDNCrypto:

    def __init__(self) -> None:

        self.encrypted_text = b''
        self.decrypted_text = ''

    def en(self, text: str) -> str:
        """
        password->uuid(去掉-)->ord->str->chr->password
        text->encode('utf-8')->b64encode->decode('utf-8')->ord->add_to_16->AES_encrypt->b64encode
        加密
        :return: list
        """
        password = ''.join(
            list(
                map(lambda x: str(x), [
                    ord(i) for i in list(str(uuid.uuid1()).replace("-", ""))
                    if not str(i).isdigit()
                ]))).replace('0', '')
        for i in [
            b64encode(
                AES.new(self.add_to_16(password[:6]),
                        AES.MODE_ECB).encrypt(self.add_to_16(str(i))))[:-2]
            for i in
            [ord(i) for i in b64encode(text.encode('utf-8')).decode('utf-8')]
        ]:
            self.encrypted_text += i
        encrypted_text = self.encrypted_text.decode()
        encrypted_text += "*"
        for i in [str(int(i) + 1) + "=" for i in self.cut(password, 1)]:
            encrypted_text += i
        return encrypted_text

    def dn(self, encrypted_text: Union[list, str]) -> str:
        """
        解密
        :param encrypted_text
        :return: None
        """
        encrypted_text = encrypted_text.split('*')
        encrypted_text_ = str(encrypted_text[-1]).split("=")
        encrypted_text_.pop()
        encrypted_text_ = ''.join(
            str(i) for i in [i for i in [int(i) - 1 for i in encrypted_text_]])
        encrypted_text.pop()
        try:
            for i in [
                AES.new(self.add_to_16(encrypted_text_[:6]),
                        AES.MODE_ECB).decrypt(
                    b64decode(i.encode() + b'==')).replace(
                    b'\x00', b'').decode() for i in
                [i + '==' for i in self.cut(''.join(encrypted_text[0]), 22)]
            ]:
                self.decrypted_text += chr(int(i))
            return b64decode(
                self.decrypted_text.encode('utf-8')).decode('utf-8')
        except UnicodeDecodeError:
            return str(b16encode('密码错了,嘿嘿'.encode('GBK')).decode('utf-8'))

    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    @staticmethod
    def cut(obj, sec):
        return [obj[i:i + sec] for i in range(0, len(obj), sec)]

    @staticmethod
    def encrypt_decrypt_image(input_file):
        with open(input_file, "wb+") as f:
            f.write(b64encode(f.read()))

    @staticmethod
    def decrypt_image(input_file, output_file):
        with open(input_file, "rb") as f:
            img_b64 = f.read()
        img_data = b64decode(img_b64)
        with open(output_file, "wb") as f:
            f.write(img_data)


if __name__ == '__main__':
    E = EDNCrypto()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--en', default='')
    parser.add_argument('-d', '--dn', default='')
    args = parser.parse_args()
    if args.dn != '':
        print(str(E.dn(args.dn)))
    if args.en != '':
        print(str(E.en(args.en)))
