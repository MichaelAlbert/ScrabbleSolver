from pathlib import Path

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
        """Returns the TrieNode corresponding to the last character of the word, 
        or None if the word doesn't exist in the Trie."""
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node
    
    def is_word(self, word) -> bool:
        """Returns True if the word exists in the Trie, False otherwise."""
        node = self.search(word)
        if node is None:
            return False
        return node.is_word
    
def build_trie_from_file(path=str) -> Trie:
    """Reads a list of words from given file and returns a Trie containing those words."""
    BASE_DIR = Path(__file__).resolve().parent
    path = BASE_DIR.parent / "data" / path
    with open(path, 'r') as f:
        words = [line.strip().lower() for line in f.readlines()]
    return Trie(words)