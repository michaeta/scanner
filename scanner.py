import fileinput
import re

tid = 0

class Token(object):
    def __init__(self, token_id, data):
        self.tid = token_id
        self.data = data
    
    def __str__(self):
        return "<Token:%s>" % self.data

class StringToken(Token):
    def __init__(self, token_id, data):
        self.tid = token_id
        self.data = data
    
    def __str__(self):
        return "<String:%s>" % self.data

class IntToken(Token):
    def __init__(self, token_id, data):
        self.tid = token_id
        self.data = data

    def __str__(self):
        return "<Int:%s>" % self.data

class BoolToken(Token):
    def __init__(self, token_id, data):
        self.tid = token_id
        self.data = data

    def __str__(self):
        return "<Bool:%s>" % self.data

class RealToken(Token):
    def __init__(self, token_id, data):
        self.tid = token_id
        self.data = data

    def __str__(self):
        return "<Real:%s>" % self.data

class StartExpr(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<StartExpr>"

class EndExpr(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<EndExpr>"

class AssignToken(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<Assign>"

class WhileToken(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<While>"

class IfToken(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<If>"

class LetToken(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<Let>"

class PrintlnToken(Token):
    def __init__(self, token_id):
        self.tid = token_id

    def __str__(self):
        return "<Println>"

class OpToken(Token):
    def __init__(self, token_id, op):
        self.tid = token_id
        self.op = op

    def __str__(self):
        return "<Op:%s>" % self.op

class TypeToken(Token):
    def __init__(self, token_id, type_name):
        self.tid = token_id
        self.type_name = type_name

    def __str__(self):
        return "<Type:%s>" % self.type_name


def new_tid():
    global tid
    tid = tid + 1
    return tid

def parse_token(token):
    string_pattern = re.compile("\"[0-9A-Za-z !,]*\"")
    real_pattern = re.compile("[-+]?[0-9]*\.[0-9]*e?")
    int_pattern = re.compile("[-+]?[0-9]+")
    bool_pattern = re.compile("true|false")
    while_pattern = re.compile("while")
    assign_pattern = re.compile("assign")
    if_pattern = re.compile("if")
    let_pattern = re.compile("let")
    println_pattern = re.compile("println")
    type_pattern = re.compile("bool|int|real|string")

    ops = re.compile("\+|and|or|not|iff|\+|-|\*|/|\^|=|<|%|logn|sin|cos|tan|e")

    if string_pattern.match(token):
        return StringToken(new_tid(), token)
    elif type_pattern.match(token):
        return TypeToken(new_tid(), token)
    elif bool_pattern.match(token):
        return BoolToken(new_tid(), token)
    elif real_pattern.match(token):
        return RealToken(new_tid(), token)
    elif int_pattern.match(token):
        return IntToken(new_tid(), token)
    elif assign_pattern.match(token):
        return AssignToken(new_tid())
    elif while_pattern.match(token):
        return WhileToken(new_tid())
    elif if_pattern.match(token):
        return IfToken(new_tid())
    elif let_pattern.match(token):
        return LetToken(new_tid())
    elif println_pattern.match(token):
        return PrintlnToken(token)
    elif ops.match(token):
        return OpToken(new_tid(), token)
    else:
        return Token(new_tid(), token)

def scan(line):
    tokens = []
    comment = re.compile("^##.*")
    if comment.match(line):
        return tokens
    curr_token = ''
    in_string = False
    for i in line:
        if i == '(':
            if curr_token != '':
                tokens.append(parse_token(curr_token))
            tokens.append(StartExpr(new_tid()))
            curr_token = ''
        elif i == ')':
            if curr_token != '':
                tokens.append(parse_token(curr_token))
            tokens.append(EndExpr(new_tid()))
            curr_token = ''
        else:
            if i != ' ':
                curr_token += i
                if i == '"':
                    if in_string:
                        in_string = False
                    else:
                        in_string = True
            elif i == ' ':
                if in_string:
                    curr_token += i
                    continue
                if curr_token != '':
                    tokens.append(parse_token(curr_token))
                curr_token = ''

    return tokens

def main():
    with open("test_case.txt") as fp:
        lines = fp.readlines()
    for line in lines:
        tokens = scan(line)
        for token in tokens:
            print token,
        print

if __name__ == "__main__":
    main()

