from modgrammar import *

grammar_whitespace_mode = 'optional'

class Integer (Grammar):
    grammar =  (WORD('0-9'))

    def value(self):
        return self.string

class Decimal1 (Grammar):
    grammar = (Integer, OPTIONAL(L('.'), OPTIONAL(Integer)))

    def value(self):
        return self.string

class Decimal2 (Grammar):
    grammar = (L('.'), Integer)

    def value(self):
        return self.string

class Decimal (Grammar):
    grammar = (Decimal1 | Decimal2)

    def value(self):
        return self.string

class Number (Grammar):
    grammar = (Decimal, OPTIONAL(L('e'), OPTIONAL(L('-')), Decimal))

    def value(self):
        return self.string

class SignedNumber(Grammar):
    grammar = (OPTIONAL(L('-')), Number)

    def value(self):
        return self.string

class Truth (Grammar):
    grammar = (L('True') | L('False'))

    def value(self):
        return self.string

class GreaterThanOp (Grammar):
    grammar = (L('('), SignedNumber, L(') > ('), SignedNumber, L(')'))

    def value(self):
        return self.string

class LessThanOp (Grammar):
    grammar = (L('('), SignedNumber, L(') < ('), SignedNumber, L(')'))

    def value(self):
        return self.string

class EqualsOp (Grammar):
    grammar = (L('('), SignedNumber, L(') = ('), SignedNumber, L(')'))

    def value(self):
        return self[0].string + self[1].value() + ') == (' + self[3].value() + self[4].string

class Condition (Grammar):
    grammar = (GreaterThanOp | LessThanOp | EqualsOp | REF('AndOp') | REF('OrOp') | REF('NotOp') | Truth)

    def value(self):
        return self[0].value()

class AndOp (Grammar):
    grammar = (L('('), Condition, L(') And ('), Condition, L(')'))

    def value(self):
        return self[0].string + self[1].value() + ') and (' + self[3].value() + self[4].string

class OrOp (Grammar):
    grammar = (L('('), Condition, L(') Or ('), Condition, L(')'))

    def value(self):
        return self[0].string + self[1].value() + ') or (' + self[3].value() + self[4].string

class NotOp (Grammar):
    grammar = (L('Not ('), Condition, L(')'))

    def value(self):
        return 'not (' + self[1].value() + self[2].string

def ParseCondition(condition):
    parser = Condition.parser()
    return parser.parse_text(condition, eof=True).value()
