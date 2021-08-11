from itertools import combinations

class Heming:

    def __init__(self, code, n, m):
        self.code = code
        self.codeL = [int(i) for i in code]
        self.n = n
        self.m = m
        self.k = n-m
        self.k_list = [[] for i in range(0,self.k)]
        self.k_ident = [2**i-1 for i in range(0,self.k)]

        self.ecode = None
        self.error_code = None
        self.ecodeT = None
        self.error_count = None
        self.decoded = None
        self.error_found = None
        self.result = None
        self.crAbility = None

    def __str__(self):
        print(self.result)

    def cr_kbits(self):
        for i in range(0,self.n):
            buf = bin(i+1)[2:]
            buf = buf.rjust(self.k, '0')
            buf = buf[::-1]
            for j in range(0,self.k):
                if (i!=j and (i not in self.k_ident)):
                    if buf[0] == '1':
                        self.k_list[j].append(i)
                    buf = buf[1:]
        return 0

    def encodeV(self):
        keys = []
        data = self.codeL.copy()
        data.reverse()

        buf = ['*' for i in range(0,self.n)]
        for i in range(0,self.n):
            if (i not in self.k_ident):
                buf[i] = data.pop(0)

        for i in self.k_list:
            k = buf[i[0]]
            for j in range(1,len(i)):
                k = k^buf[i[j]]
            keys.append(k)
  
        for i in range(0,self.n):
            if (i in self.k_ident):
                buf[i] = keys.pop(0)

        buf.reverse()
        buf = [str(i) for i in buf]
        self.ecode = ''.join(buf)
        return 0

    def transfer_error(self, error_code=''):
        self.error_code = error_code

        result = bin(int(self.ecode, base = 2)^int(error_code, base = 2))[2:]
        result = result.rjust(self.n,'0')

        self.ecodeT = result
        self.error_count = error_code.count('1')

        return 0

    def decodeV(self):
        error_found = 0

        buf = [int(i) for i in self.ecodeT]
        buf.reverse()

        for i in range(0,self.error_count):
            keys = []
            ct = 0

            for i in self.k_list:
                h = buf[self.k_ident[ct]]
                for j in range(0,len(i)):
                    h = h^buf[i[j]]
                keys.append(h)
                ct += 1

            keys.reverse()
            keys = [str(i) for i in keys]
            k = int(''.join(keys), base = 2) - 1

            if (k!=0):
                error_found += 1
                buf[k] = int(bool(buf[k]-1))
        
        buff = buf.copy()
        buf.reverse()
        buf = [str(i) for i in buf]
        buf = ''.join(buf)

        self.decoded = buf
        self.error_found = error_found

        shift = 0
        for i in self.k_ident:
            buff.pop(i-shift)
            shift += 1
        
        buff.reverse()
        self.result = ''.join([str(i) for i in buff])

        return 0

    def Correction_ability(self):
        self.crAbility = 1/len(list(combinations(range(1,self.n+1), self.error_found)))
        return 0

    def print_variables(self, var_name = ''):
        var = var_name.split()
        variables = ['code', 'codeL', 'ecode', 'error_code', 'ecodeT', 'error_count', 'decoded', 'error_found','result', 'crAbility']
        messages = [
         f'Код изначального вектора: {self.code}',
         f'Код изначального вектора в виде массива: {self.codeL}',
         f'Закодированное сообщение с помощью кода Хемминга [{self.n},{self.m}]: {self.ecode}', 
         f'Код вектора ошибки: {self.error_code}',
         f'Код вектора, переданного с ошибкой: {self.ecodeT}', 
         f'Количество ошибок: {self.error_count}',
         f'Исправленный вектор: {self.decoded}',
         f'Кол-во найденных ошибок: {self.error_found}',
         f'Декодированный вектор: {self.result}',
         f'Кооректирующая способность кода: {self.crAbility}'
         ]

        for i in var:
            index = variables.index(i)
            if ( index != -1):
                print(messages[index])
    

while True:
    msg = input('\nВведите информацию в таком виде без скобок: (код_вектора N M)\n')
    if (msg == 'exit'):
        break
    try:
        code,n,m = msg.split()
        n,m = map(int,[n,m])
    except ValueError:
        print('Информация введена неправильно')
    cl = Heming(code,n,m)
    cl.cr_kbits()
    cl.encodeV()
    cl.transfer_error(input('Введите вектор ошибки: '))
    cl.decodeV()
    cl.Correction_ability()
    cl.print_variables('code ecode error_code ecodeT decoded result error_count error_found crAbility')