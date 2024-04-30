class TrieNode:
    def __init__(self):
        self.parent = None
        self.upperEdge = None
        self._isEnd = False
        self.values = []
        self.children = {}


class Trie:
    def __init__(self, nodes=None, caseInsensitive=True):
        self.root = TrieNode()
        self.count = 0
        self.charset = set()
        self.charsetAscending = []
        self.charsetDescending = []
        self.caseInsensitive = caseInsensitive
        if nodes is None:
            nodes = []
        self.create_trie(nodes)

    def _push_all_next_sub_strings(self, current_node, prefix, queue, reverse=False):
        charset = sorted(current_node.children.keys(), reverse=reverse)
        for ch in charset:
            queue.append((current_node.children[ch], prefix + ch))

    def _push_all_next_nodes(self, current_node, queue, reverse=False):
        charset = sorted(current_node.children.keys(), reverse=reverse)
        for ch in charset:
            queue.append(current_node.children[ch])

    def _round(self, node, ceil=True):
        current_node = node
        queue = [current_node]

        while queue:
            current_node = queue.pop()
            self._push_all_next_nodes(current_node, queue, ceil)

            if current_node._isEnd:
                return current_node

    def _get_max(self, node):
        return self._round(node)

    def _get_min(self, node):
        return self._round(node, False)

    def _get_prefix(self, node):
        current_node = node
        prefix = ''
        while current_node.parent:
            prefix = current_node.upperEdge + prefix
            current_node = current_node.parent
        return prefix

    def _binary_search_ascending(self, array, value):
        start = 0
        end = len(array) - 1

        while start <= end:
            mid = (start + end) // 2
            if value < array[mid]:
                end = mid - 1
            elif array[mid] <= value:
                start = mid + 1

        return start

    def _binary_search_descending(self, array, value):
        start = 0
        end = len(array) - 1

        while start <= end:
            mid = (start + end) // 2
            if value > array[mid]:
                end = mid - 1
            elif array[mid] >= value:
                start = mid + 1

        return start

    def _find_preorder_predecessor_values(self, queue):
        predecessor_values = None
        i = len(queue)
        while i > 0:
            i -= 1
            current_node, next_ch = queue[i]
            searching_charset = sorted(
                self.charsetDescending[self._binary_search_descending(self.charsetDescending, next_ch):])
            for ch in searching_charset:
                if ch in current_node.children:
                    predecessor_values = self._get_max(current_node.children[ch]).values
                    break
            if predecessor_values is not None or current_node._isEnd:
                predecessor_values = current_node.values
                break

        return predecessor_values

    def _find_preorder_successor_values(self, queue):
        successor_values = None
        i = len(queue)
        while i > 0:
            i -= 1
            current_node, next_ch = queue[i]
            searching_charset = sorted(
                self.charsetAscending[self._binary_search_ascending(self.charsetAscending, next_ch):])
            for ch in searching_charset:
                if ch in current_node.children:
                    successor_values = self._get_min(current_node.children[ch]).values
                    break

        return successor_values

    def _find_node(self, key):
        current_node = self.root
        for ch in key:
            if ch not in current_node.children:
                return None
            current_node = current_node.children[ch]

        return current_node

    def _get_all_possible_nodes_for_prefix(self, prefix):
        queue = []
        if self.caseInsensitive:
            prefix = prefix.lower()
        current_node = self.root
        curr_i = 0
        for ch in prefix:
            if ch not in current_node.children:
                queue.append((current_node, ch))
                break
            queue.append((current_node, ch))
            current_node = current_node.children[ch]
            curr_i += 1

        return curr_i, current_node, queue

    def get_preorder_predecessor_and_successor_for_new_key(self, key):
        if self.caseInsensitive:
            key = key.lower()
        curr_i, current_node, queue = self._get_all_possible_nodes_for_prefix(key)

        predecessor_values = self._find_preorder_predecessor_values(queue)
        successor_values = None
        if curr_i == len(key):
            successor_values = self._get_min(current_node).values
        elif curr_i < len(key):
            successor_values = self._find_preorder_successor_values(queue)

        return predecessor_values, successor_values

    def get_preorder_predecessor_and_successor_for_existing_key(self, key):
        if self.caseInsensitive:
            key = key.lower()
        curr_i, current_node, queue = self._get_all_possible_nodes_for_prefix(key)

        predecessor_values = self._find_preorder_predecessor_values(queue)
        queue_copy = queue.copy()
        successor_values = self._find_preorder_successor_values(queue_copy)

        return predecessor_values, successor_values

    def create_trie(self, nodes):
        for node in nodes:
            self.insert(node[0], node[1])

    def insert(self, key, value):
        is_added_new_char = False
        current_node = self.root

        for ch in key.lower() if self.caseInsensitive else key:
            if ch not in self.charset:
                is_added_new_char = True
                self.charset.add(ch)
                self.charsetAscending.append(ch)

            if ch not in current_node.children:
                current_node.children[ch] = TrieNode()
                current_node.children[ch].parent = current_node
                current_node.children[ch].upperEdge = ch
            current_node = current_node.children[ch]

        current_node._isEnd = True
        current_node.values.append(value)

        if is_added_new_char:
            self.charsetAscending.sort()
            self.charsetDescending = self.charsetAscending[::-1]

        self.count += 1

    def find(self, key):
        node = self._find_node(key.lower() if self.caseInsensitive else key)
        return node.values if node and node._isEnd else None

    def remove(self, key, value_checker):
        node = self._find_node(key.lower() if self.caseInsensitive else key)
        if not node or not node._isEnd:
            return False

        for index, value in enumerate(node.values):
            if value_checker(value):
                del node.values[index]
                break

        if not node.values:
            node._isEnd = False
        self.count -= 1
        return True

    def search(self, skip=0, limit=None, prefix=None, contains=None, reverse=False):
        result = []
        queue = [(self.root, '')]
        count = 0

        if prefix:
            prefix = prefix.lower() if self.caseInsensitive else prefix
            current_node = queue.pop()[0]
            for ch in prefix:
                current_node = current_node.children.get(ch)
                if not current_node:
                    return []

            self._push_all_next_sub_strings(current_node, prefix, queue, reverse)
            if current_node._isEnd:
                queue.append((current_node, prefix))

        while queue:
            current_node, curr_prefix = queue.pop()
            self._push_all_next_sub_strings(current_node, curr_prefix, queue, reverse)

            if current_node._isEnd:
                if contains and contains not in curr_prefix:
                    continue
                if count < skip:
                    count += 1
                    continue

                result.append({'currPrefix': curr_prefix, 'values': current_node.values})
                if limit is not None and len(result) == limit:
                    return result

        return result


def main():
    trie = Trie()
    with open('list.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            word = line.strip()
            trie.insert(word, word)

    search_word = input("Enter a word to search: ").strip()
    result = trie.find(search_word)
    if result:
        print("Found:", result)
    else:
        print("Word not found.")


if __name__ == "__main__":
    main()
