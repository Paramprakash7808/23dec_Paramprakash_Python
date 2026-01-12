import random

print("Random Number From 0 to 1:",random.random())
print("Random Number From 1 to 100:",random.randint(1,100))

sub = ['c','c++','sql','dbms','python']
print("Random Choice of Subject:",random.choice(sub))

sub = ['c','c++','sql','dbms','python']
random.shuffle(sub)
print("Shuffle of Subject:",sub)