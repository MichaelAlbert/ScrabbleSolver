class TrieNode:
    def __init__(self, is_word=False):
        self.children = {}
        self.is_word = is_word

class Trie:
    def __init__(self, words):
        self.root = TrieNode(False)
        for word in words:
            current_node= self.root
            for char in word:
                if char not in current_node.children:
                    current_node.children[char] = TrieNode(False)
                current_node = current_node.children[char]
            current_node.is_word = True
    
    def search(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node
    
    def is_word(self, word) -> bool:
        node = self.search(word)
        if node is None:
            return False
        return node.is_word
    
def word_list(path=str) -> Trie:
    with open(path, 'r') as f:
        words = [line.strip() for line in f.readlines()]
    return Trie(words)