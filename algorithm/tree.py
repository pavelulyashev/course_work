#! /usr/bin/env python

class Weight(object):
    def __init__(self, *args):
        self._tuple = args[:3]

    def __str__(self):
        return '(%d, %d | %d)' % self._tuple

    def __getitem__(self, index):
        return self._tuple[index-1]

    def __eq__(self, other):
        return self._tuple == other._tuple

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        self._check_inst(other)
        res = self[1] >= other[1]
        for i in range(2, len(self._tuple)):
            res_i = sum(self._tuple[:i]) >= sum(other._tuple[:i])
            if res_i ^ res:
                return None
        return res
        
    def __gt__(self, other):
        res = self >= other
        return None if res is None else (res and self != other)
        
    def __le__(self, other):
        res = self >= other
        return None if res is None else (not res)

    def __lt__(self, other):
        res = self >= other
        return None if res is None else (not res or self == other)

    def _check_inst(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        if len(self._tuple) != len(other._tuple):
            raise IndexError
        if sum(self._tuple) != sum(other._tuple):
            raise ValueError
        
    @property
    def as_tuple(self):
        return self._tuple


class WeightTree(object):
    def __init__(self, r):
        self._tree = {}
        for m3 in range(r + 1):
            self._tree[m3] = tuple(Weight(m1, r - m3 - m1, m3) \
                    for m1 in range(0, r - m3 + 1)
                    if m1 >= r - m3 - m1 and (r - m1 - m3 > 0 or m3 == 0))

    def __str__(self):
        tree = self._tree_for_rendering()
        res = ''
        keys = tree.keys()
        keys.sort()
        keys.reverse()
        for i in keys:
            res = res + tree[i] + '\n'
        return res

    def _tree_for_rendering(self):
        tree = {}
        offset = 0
        between = 2
        for m3 in self._tree:
            level_width = 0
            for wei in self._tree[m3]:
                width = len(wei.__str__())
                if width > level_width:
                    level_width = width

            for wei in self._tree[m3]:
                rendered_wei = wei.__str__()
                width = len(rendered_wei)
                diff = wei[1] - wei[3]
                if not tree.has_key(diff):
                    tree[diff] = ' ' * offset
                tree[diff] = tree[diff] + rendered_wei.replace('|' , 
                                 ' ' * (level_width - width) + '|') + \
                             ' ' * between

            offset += level_width + between
        return tree



if __name__ == '__main__':
    w = Weight(4, 1, 1)
    r = Weight(3, 3, 0)
    #print(w)
    #print(w == Weight(3, 2, 3))
    tree = WeightTree(1999)
    f = open('test_tree.txt', 'w')
    f.write(tree.__str__())
    f.close()
    print('file written')

