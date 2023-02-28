import datetime
import json
import os
import pkgutil
import platform
import random
import sys
import tempfile
import threading
import time

import colorama
import requests


lock = threading.Lock()
colorama.init()
fg = [
    '\033[91;1m',
    '\033[92;1m',
    '\033[93;1m',
    '\033[94;1m',
    '\033[95;1m',
    '\033[96;1m',
    '\033[97;1m',
    '\033[90;1m'
]

# CACERT FIX
cert_data = pkgutil.get_data('certifi', 'cacert.pem')

# Write the cert data to a temporary file
handle = tempfile.NamedTemporaryFile(delete=False)
handle.write(cert_data)
handle.flush()

# Set the temporary file name to an environment variable for the requests package
os.environ['REQUESTS_CA_BUNDLE'] = handle.name


def ntime():
    return datetime.datetime.now().strftime('%H:%M:%S')

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


class BFreakFramework:
    def __init__(self):
        self.load_json()
        self.banner()
        self.menu()

    def load_json(self):
        print('{}[+] Loading Carrier Database....'.format(fg[1]))
        self.data = requests.get('https://sh0g0.pythonanywhere.com/sh0g0_data.json').json()
        clear()

    def banner(self):
        # region Banner
        print('''{0}▄   ▄ {1}BFreak
{0}█▀█▀█ {1}Framework
{0}█▄█▄█
 ███  ▄▄
 ████▐█ █
 ████   █
 ▀▀▀▀▀▀▀
'''.format(fg[7], fg[1]))
        # endregion Banner

    def menu(self):
        print('''
{0}BFreak Framework Menu
{1}━━━┳━━━━━━━━━━━━━━━━━
   ┣━[ {2}01 {3}: {4}Number Carrier Checker
   {1}┣━[ {2}02 {3}: {4}Generate Numbers {3}({5}State{3})
   {1}┣━[ {2}03 {3}: {4}Generate Numbers {3}({5}Area Code{3})
   {1}┗━[ {2}04 {3}: {4}Generate Numbers {3}({5}Prefix{3})
'''.format(fg[6], fg[5], fg[0], fg[2], fg[1], fg[3]))
        print('\t{0}╭╼[ {5}BFreakFramework {0}]╾╼[ {1}Enter{4}/{1}Choice {0}]\n\t╰─╼ {2}'.format(fg[5], fg[6], fg[1], fg[3], fg[2], fg[0]), end='')
        choice = input('')
        if choice in ['1', '01']:
            self.load()
            self.execute()
        elif choice in ['2', '02']:
            self.gen_state()
        elif choice in ['3', '03']:
            self.gen_area_code()
        elif choice in ['4', '04']:
            self.gen_prefix()

    def load(self):
        if not os.path.isdir('Carriers'):
            os.mkdir('Carriers')
        is_numbers = False
        while not is_numbers:
            print('\t{0}╭╼[ {5}BFreakFramework {0}]╾╼[ {1}Enter {3}Numbers{1} List {4}Filename {0}]\n\t╰─╼ {2}'.format(fg[5], fg[6], fg[1], fg[3], fg[2], fg[0]), end='')
            filename = input('').replace('"', '').replace('\'', '')
            if '.txt' not in filename:
                filename = filename + '.txt'
            if not os.path.isfile(filename):
                print('\t{0}[{1}ERROR{0}] {1}- {2}File Not Found!'.format(fg[5], fg[0], fg[6]), end='\r')
                time.sleep(1)
                print(' ' * 45)
                continue
            else:
                with open(filename) as file:
                    self.numbers = [x for x in file.read().splitlines() if x]
                if len(self.numbers) < 2:
                    print('\t{0}[{1}ERROR{0}] {1}- {2}Please enter numbers list on file!'.format(fg[5], fg[0], fg[6]), end='\r')
                    time.sleep(1)
                    print(' ' * 55)
                    continue
                is_numbers = True
        self.number_fn = filename

    def execute(self):
        def worker():
            while True:
                try:
                    number = self.numbers.pop()
                except IndexError:
                    break

                try:
                    self.check(number)
                except:
                    pass

        print('\t{0}╭╼[ {5}BFreakFramework {0}]╾╼[ {1}Thread{4}/{1}Workers {0}]\n\t╰─╼ {2}'.format(fg[5], fg[6], fg[1], fg[3], fg[2], fg[0]), end='')
        workers = int(input(''))
        for _ in range(workers):
            t = threading.Thread(target=worker)
            t.start()

    def check(self, number):
        if number.startswith('1') and len(number) == 11:
            number = number[1:]
        if number.startswith('+1'):
            number = number.replace('+1', '')
        number = number.replace('-', '')
        prefix = number[:6]
        if prefix in list(self.data.keys()):
            info = self.data[prefix]
            city = info['city']
            state = info['state']
            pn_carrier = info['carrier']
            pn_type = info['type']
            if pn_type == 'Landline':
                with lock:
                    print('\t{0}[{1}{2}{0}] - {3}({4}{5}{3}) {6}{7}{0}|{6}{8}{0}|{6}{9}{0}|{6}{10}{0}'.format(
                        fg[5], fg[4], ntime(), fg[3], fg[0], pn_carrier, fg[1], number, pn_type, city, state
                    ))
            else:
                with lock:
                    print('\t{0}[{1}{2}{0}] - {3}({4}{5}{3}) {6}{7}{0}|{6}{8}{0}|{6}{9}{0}|{6}{10}{0}'.format(
                        fg[5], fg[4], ntime(), fg[3], fg[2], pn_carrier, fg[1], number, pn_type, city, state
                    ))
                with open(f'Carriers/{pn_carrier}.txt', 'a+') as file:
                    file.write(f'{number}\n')
        else:
            with lock:
                print('\t{0}[{1}{2}{0}] - {3}({4}{5}{3}) {6}{7}'.format(fg[5], fg[4], ntime(), fg[3], fg[0], 'DEAD', fg[1], number))

    def gen_state(self):
        if not os.path.isdir('State'):
            os.mkdir('State')
        prefixes = []
        is_done = False
        while not is_done:
            print('\t{0}╭╼[ {5}BFreakFramework {0}]╾╼[ {1}Enter{4}/{1}State {0}]\n\t╰─╼ {2}'.format(fg[5], fg[6], fg[1], fg[3], fg[2], fg[0]), end='')
            state = str(input('')).capitalize()
            if ' ' in state:
                parts = state.split(' ')
                final = []
                for part in parts:
                    final.append(part.capitalize())
                state = ' '.join(final)
            if f'"state": "{state}"' in json.dumps(self.data):
                is_done = True
                if not os.path.isdir(f'State/{state}'):
                    os.mkdir(f'State/{state}')
            else:
                print(f'\t{fg[0]}[!] - Please enter a valid state!', end='\r')
                time.sleep(0.5)
        for k, v in self.data.items():
            if v['state'] == state and v['type'] == 'Mobile':
                prefixes.append(k)
        
        def gen_prefix(prefix):
            results = ['1{}{}'.format(prefix, '{}{}'.format('0' * (4-len(str(num))), num)) for num in range(1, 10000)]
            random.shuffle(results)
            result = '\n'.join(results)
            with lock:
                print('\t{0}({1}{2}{0}) - [{3}{4}{0}] {5}Generated...'.format(fg[0], fg[4], ntime(), fg[1], prefix, fg[6]))
            with open(f'State/{state}/{prefix}.txt', 'a+') as file:
                file.write(f'{result}\n')
        
        def worker():
            while True:
                try:
                    prefix = prefixes.pop()
                except IndexError:
                    break

                try:
                    gen_prefix(prefix)
                except:
                    pass

        for _ in range(len(prefixes)):
            t = threading.Thread(target=worker)
            t.start()

    def gen_area_code(self):
        if not os.path.isdir('AreaCode'):
            os.mkdir('AreaCode')
        prefixes = []
        is_done = False
        while not is_done:
            print('\t{0}╭╼[ {5}BFreakFramework {0}]╾╼[ {1}Enter{4}/{1}AreaCode {0}]\n\t╰─╼ {2}'.format(fg[5], fg[6], fg[1], fg[3], fg[2], fg[0]), end='')
            area_code = str(input('')).capitalize()
            if any(area_code in x[:3] for x in list(self.data.keys())):
                is_done = True
                if not os.path.isdir(f'AreaCode/{area_code}'):
                    os.mkdir(f'AreaCode/{area_code}')
            else:
                print(f'\t{fg[0]}[!] - Please enter a valid area code!', end='\r')
                time.sleep(0.5)
        for k, v in self.data.items():
            if area_code in k[:3] and v['type'] == 'Mobile':
                prefixes.append(k)
        
        def gen_prefix(prefix):
            results = ['1{}{}'.format(prefix, '{}{}'.format('0' * (4-len(str(num))), num)) for num in range(1, 10000)]
            random.shuffle(results)
            result = '\n'.join(results)
            with lock:
                print('\t{0}({1}{2}{0}) - [{3}{4}{0}] {5}Generated...'.format(fg[0], fg[4], ntime(), fg[1], prefix, fg[6]))
            with open(f'AreaCode/{area_code}/{prefix}.txt', 'a+') as file:
                file.write(f'{result}\n')
        
        def worker():
            while True:
                try:
                    prefix = prefixes.pop()
                except IndexError:
                    break

                try:
                    gen_prefix(prefix)
                except:
                    pass

        for _ in range(len(prefixes)):
            t = threading.Thread(target=worker)
            t.start()

    def gen_prefix(self):
        if not os.path.isdir('Prefix'):
            os.mkdir('Prefix')
        prefixes = []
        is_done = False
        while not is_done:
            print('\t{0}╭╼[ {5}BFreakFramework {0}]╾╼[ {1}Enter{4}/{1}Prefix {0}]\n\t╰─╼ {2}'.format(fg[5], fg[6], fg[1], fg[3], fg[2], fg[0]), end='')
            prefix = str(input('')).capitalize()
            if prefix in list(self.data.keys()):
                is_done = True
            else:
                print(f'\t{fg[0]}[!] - Please enter a valid prefix!', end='\r')
                time.sleep(0.5)
        
        def gen_prefix(prefix):
            results = ['1{}{}'.format(prefix, '{}{}'.format('0' * (4-len(str(num))), num)) for num in range(1, 10000)]
            random.shuffle(results)
            result = '\n'.join(results)
            with lock:
                print('\t{0}({1}{2}{0}) - [{3}{4}{0}] {5}Generated...'.format(fg[0], fg[4], ntime(), fg[1], prefix, fg[6]))
            with open(f'Prefix/{prefix}.txt', 'a+') as file:
                file.write(f'{result}\n')
        
        gen_prefix(prefix)


if __name__ == '__main__':
    try:
        BFreakFramework()
    except KeyboardInterrupt:
        sys.exit()

