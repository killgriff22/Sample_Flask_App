defualtexpect="1234567890ZXCVBNM<>?ASDFGHJKL:QWERTYUIOP}[|~!@#$%^&*()_+zxcvbnm,./asdfghjkl;qwertyuiop[]"
class x4x5:
    def generatekey(expect=defualtexpect):
        import random
        codes=[]
        random.seed(expect)
        for char in expect:
            code=""
            for i in range(4):
                code+=random.choice(expect)
            code += char
            codes.append(code)
        key=""
        random.shuffle(codes)
        for code in codes:
            key+=code
        return key
    def decrypt(key,msg):
        keys=[key[i:i+5] for i in range(0, len(key), 5)]
        msg = [msg[i:i+4] for i in range(0, len(msg), 4)]
        decrypted=""
        for partkey in msg:
            for fullkey in keys:
                if partkey in fullkey:
                    decrypted += fullkey[4]
        return decrypted
    def encrypt(key,msg):
        encoded=""
        keys= [key[i:i+5] for i in range(0, len(key), 5)]
        for char in msg:
            for key in keys:
                if key[4] == char:  encoded+=[key[i:i+4] for i in range(0, len(key), 4)][0]
        return encoded