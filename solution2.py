# time complexity o(n)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix_suffix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

class DictionarySearch:
    def __init__(self, words):
        self.trie = Trie()
        for word in words:
            self.trie.insert(word)

    def search(self, text):
        matches = set()
        n = len(text)
        for i in range(n):
            
            if self.trie.search_prefix_suffix(text[i:]):
                matches.add(text[i:])
            node = self.trie.root
            for j in range(i, -1, -1):
                if text[j] not in node.children:
                    break
                node = node.children[text[j]]
                if node.is_end_of_word:
                    matches.add(text[j:i+1])
          
            node = self.trie.root
            for j in range(i, n):
                if text[j] not in node.children:
                    break
                node = node.children[text[j]]
                if node.is_end_of_word:
                    matches.add(text[i:j+1])
        return matches


dictionary = []
with open('list.txt', 'r') as file:
    for line in file:
        word = line.strip()
        dictionary.append(word)


searcher = DictionarySearch(dictionary)
search_text = input("Enter the search text: ")
result = searcher.search(search_text)
print("Matches found:", result)
