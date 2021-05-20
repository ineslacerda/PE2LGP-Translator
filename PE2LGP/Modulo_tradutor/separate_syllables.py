class char():
    def __init__(self):
        pass
    
class char_line():
    def __init__(self, word):
        self.word = word
        self.char_line = [(char, self.char_type(char)) for char in word]
        self.type_line = ''.join(chartype for char, chartype in self.char_line)
        
    def char_type(self, char):
        if char in set(['a', 'e', 'i', 'o', 'u']):
            return 'v'
        if char=='x':
            return 'x'
        if char=='s':
            return 's'
        else:
            return 'c'
            
    def find(self, finder):
        return self.type_line.find(finder)
        
    def split(self, pos, where):
        return char_line(self.word[0:pos+where]), char_line(self.word[pos+where:])
    
    def split_by(self, finder, where):
        split_point = self.find(finder)
        if split_point!=-1:
            chl1, chl2 = self.split(split_point, where)
            return chl1, chl2
        return self, False
     
    def __str__(self):
        return self.word
    
    def __repr__(self):
        return repr(self.word)

class silabizer():
    def __init__(self):
        self.grammar = []
        self.mapping = {'a': 'A', 'i': 'E', 'e': 'A', 'o': 'O', 'u': 'U', 'b': 'B', 'm': 'B', 'p': 'B', 'f': 'F', 'v': 'F'}
        
    def split(self, chars):
        rules  = [('cccc',2), ('xcc',1), ('ccx',2), ('csc',2), ('xc',1), ('cc',1), ('vcc',2), ('sc',1), ('cs',1), ('vc',1), ('vs',1), ('ccvv', 3)]
        for split_rule, where in rules:
            first, second = chars.split_by(split_rule,where)
            if second:
                if first.type_line in set(['c','s','x','cs']) or second.type_line in set(['c','s','x','cs']):
                    continue
                if first.type_line[-1]=='c' and second.word[0] in set(['l','r']):
                    continue
                if first.word[-1]=='l' and second.word[-1]=='h':
                    continue
                if first.word[-1]=='r' and second.word[-1]=='r':
                    continue
                if first.word[-1]=='c' and second.word[-1]=='h':
                    continue
                return self.split(first)+self.split(second)
        
        chars = list(str(chars))
        for index in range(0,len(chars)):
            if chars[index] in self.mapping.keys():
                chars[index] = self.mapping[chars[index]]
            elif index>1:
                chars[index] = ""
            elif index <= 1:
                chars[index] = "C"
            if index > 0 and chars[index-1] == chars[index]:
                chars[index] = ""
        chars = ''.join(chars)
        return [chars]
        
    def __call__(self, word):
        return self.split(char_line(word))