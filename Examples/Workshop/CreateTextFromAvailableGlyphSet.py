a = u"""
(CNN) It’s one thing to hear

glyphs = set(('a', 'b', 'c', 'g', 's', 'h', 'r', 'e', 'z', 'n', 'd', ' '))

def isValidWord(word):
    for c in word:
        if not c in glyphs:
            return False
    return True
        
words = a.split(' ')
output = []
for word in words:
    if isValidWord(word):
        output.append(word)

print ' '.join(output)
