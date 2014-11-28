import unittest2

class TestKey(unittest2.TestCase):
    def _getTargetClass(self):
        from .key import Key
        return Key

    def test__init__w_flat(self):
        klass = self._getTargetClass()
        k = klass(flat=['ParentModel', 42, 'Model', 'foobar'])
        self.assertEqual(k._path, [{"kind":'ParentModel', "id": 42}, {"kind":'Model', "name":'foobar'}])

    def test__init__w_pair(self):
        klass = self._getTargetClass()
        k = klass(pairs=[("ParentModel", 42), ('Model', 'foobar')])
        self.assertEqual(k._path, [{"kind":'ParentModel', "id": 42}, {"kind":'Model', "name":'foobar'}])

    def test__init__w_path(self):
        klass = self._getTargetClass()
        k = klass(path=[{"kind":'ParentModel', "id": 42}, {"kind":'Model', "name":'foobar'}])
        self.assertEqual(k._path, [{"kind":'ParentModel', "id": 42}, {"kind":'Model', "name":'foobar'}])
