import codecs

class StrHexCrypt(object):
    def __init__(self, text: str, salt: int, revert=False):
        self.salt = salt
        self.text = text
        if revert:
            self.text = self.decrypting()
        else:
            self.text = self.encrypting()

    def decrypting(self):
        temp = self.split_n_fuse(self.text)
        for _ in range(1, self.salt):
            x = self.salt - _
            temp[0] = str(hex((int(temp[0], base=16) ^ x) % 254))[2:]
            if len(temp[0]) == 1:
                temp[0] = '0' + temp[0]
                #print(temp[0])
            temp = self.shift_pos(temp, shift_range=_+1, pos=0, vector='left')
            temp = self.shift_pos(temp, shift_range=_+1, pos=1, vector='right')
            #print(temp)
        #print(x)
        return self.plain_to_hex(self.invert_pos(temp), reverse=True)

    def encrypting(self):
        temp = self.invert_pos(self.plain_to_hex(self.text))
        #print(temp)
        for _ in range(1, self.salt):
            temp = self.shift_pos(temp, shift_range=_+1, pos=1, vector='left')
            temp = self.shift_pos(temp, shift_range=_+1, pos=0, vector='right')
            x = _
            temp[0] = str(hex((int(temp[0], base=16) ^ x) % 254))[2:]
            if len(temp[0]) == 1:
                temp[0] = '0' + temp[0]
            #print(temp)
        #print(x)
        return self.split_n_fuse(temp)

    def plain_to_hex(self, get, reverse=False):
        if reverse:
            temp = self.split_n_fuse(get)
            binary_str = codecs.decode(temp, "hex")
            return str(binary_str, 'utf-8')
        else:
            temp = ''
            for letter in get.encode():
                t = hex(letter)
                temp += str(t)[2:]
            return self.split_n_fuse(temp)

    def split_n_fuse(self, input):
        if type(input) == str:
            t = []
            for i in range(0, len(input) // 2):
                x = i * 2
                t.append(input[x:x + 2])
            return t
        elif type(input) == list:
            t = ''
            for i in input:
                t += i
            return t

    def shift_pos(self, hex_arr, shift_range=1, pos=0, vector='right'):
        for _ in range(0, shift_range):
            crypted_arr = []
            if vector == 'right':
                hold = hex_arr[-1][pos]
                for hex in hex_arr:
                    string = ''
                    for i in range(len(hex)):
                        if i != pos:
                            string += hex[i]
                        else:
                            string += hold
                            hold = hex[i]
                    crypted_arr.append(string)
            elif vector == 'left':
                hold = hex_arr[0][pos]
                for hex in hex_arr[::-1]:
                    string = ''
                    for i in range(len(hex)):
                        if i != pos:
                            string += hex[i]
                        else:
                            string += hold
                            hold = hex[i]
                    crypted_arr.append(string)
            return crypted_arr

    def invert_pos(self, hex_arr):
        return hex_arr[::-1]

text = 'Hello whats up ma dude mal schauen ob die länge des textes etwas an dem resultat ändert'
if __name__ == '__main__':
    for i in range(1, 200):
        ss = StrHexCrypt(text, i)
        text = ss.text
        print(text)
        ss = StrHexCrypt(text, i, revert=True)
        text = ss.text
        print(text)
