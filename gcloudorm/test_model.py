import unittest2

class TestModel(unittest2.TestCase):
    def testModel(self):
        import model
        import key

        # key name
        m = model.Model(id='bar')
        self.assertEqual(m.key().name(), 'bar')
        self.assertEqual(m.key().kind(), 'Model')

        p = key.Key('ParentModel', 'foo')

        # key name + parent
        m = model.Model(id='bar', parent=p)
        self.assertEqual(m.key().path(), key.Key(flat=('ParentModel', 'foo', 'Model', 'bar')).path())

        # key id
        m = model.Model(id=42)
        self.assertEqual(m.key().id(), 42)

        # key id + parent
        m = model.Model(id=42, parent=p)
        self.assertEqual(m.key().path(), key.Key(flat=('ParentModel', 'foo', 'Model', 42)).path())

        # parent
        m = model.Model(parent=p)
        self.assertEqual(m.key().path(), key.Key(flat=('ParentModel', 'foo', 'Model', None)).path())

