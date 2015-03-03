import unittest2
from gcloudorm import model
from gcloud import datastore
from gcloud.datastore.key import Key
from gcloud.datastore.connection import Connection

class TestModel(unittest2.TestCase):
    def setUp(self):
        from gcloud import datastore
        datastore.set_defaults(dataset_id="test-data-set", connection=Connection())

    def testModel(self):
        # key name
        m = model.Model(id='bar')
        self.assertEqual(m.key.name, 'bar')
        self.assertEqual(m.key.kind, 'Model')

        p = Key('ParentModel', 'foo')

        # key name + parent
        m = model.Model(id='bar', parent=p)
        self.assertEqual(m.key.path, Key('ParentModel', 'foo', 'Model', 'bar').path)

        # key id
        m = model.Model(id=42)
        self.assertEqual(m.key.id, 42)

        # key id + parent
        m = model.Model(id=42, parent=p)
        self.assertEqual(m.key.path, Key('ParentModel', 'foo', 'Model', 42).path)

        # parent
        m = model.Model(parent=p)
        self.assertEqual(m.key.path, Key('ParentModel', 'foo', 'Model').path)

    def testBooleanProperty(self):
        class TestModel(model.Model):
            test_bool = model.BooleanProperty()

        m = TestModel()
        self.assertEqual(m.test_bool, None)
        self.assertEqual(m['test_bool'], None)

        m = TestModel(test_bool=False)
        self.assertEqual(m.test_bool, False)
        self.assertEqual(m['test_bool'], False)

        m.test_bool = True
        self.assertEqual(m.test_bool, True)
        self.assertEqual(m['test_bool'], True)

        class TestModel(model.Model):
            test_bool = model.BooleanProperty(default=True)

        m = TestModel()
        self.assertEqual(m.test_bool, True)
        self.assertEqual(m['test_bool'], True)

    def testIntegerProperty(self):
        class TestModel(model.Model):
            test_int = model.IntegerProperty()

        m = TestModel()
        self.assertEqual(m.test_int, None)
        self.assertEqual(m['test_int'], None)

        class TestModel(model.Model):
            test_int = model.IntegerProperty(default=3)

        m = TestModel()
        self.assertEqual(m['test_int'], 3)

        m.test_int = 4
        self.assertEqual(m.test_int, 4)
        self.assertEqual(m['test_int'], 4)

    def testFloatproperty(self):
        class TestModel(model.Model):
            test_float = model.FloatProperty()

        m = TestModel()
        self.assertEqual(m.test_float, None)
        self.assertEqual(m['test_float'], None)

        class TestModel(model.Model):
            test_float = model.FloatProperty(default=0.1)

        m = TestModel()
        self.assertEqual(m['test_float'], 0.1)

        m.test_float = 0.2
        self.assertEqual(m['test_float'], 0.2)

    def testTextProperty(self):
        class TestModel(model.Model):
            test_text = model.TextProperty()

        m = TestModel()
        self.assertEqual(m.test_text, None)


        class TestModel(model.Model):
            test_text = model.TextProperty(default="")

        m = TestModel()
        self.assertEqual(m['test_text'], "")


    def testStringProperty(self):
        class TestModel(model.Model):
            test_str = model.StringProperty()

        m = TestModel()
        self.assertEqual(m.test_str, None)
        m.test_str = '123'

        self.assertEqual(m['test_str'], '123')


    def testPickleProperty(self):
        class TestModel(model.Model):
            test_pickle = model.PickleProperty()

        m = TestModel()
        self.assertEqual(m.test_pickle, None)
        m = TestModel(test_pickle={"123": "456"})
        self.assertEqual(m.test_pickle, {"123": "456"})

        m.test_pickle = {'456': '789'}
        self.assertEqual(m.test_pickle, {'456': '789'})

    def testJsonProperty(self):
        class TestModel(model.Model):
            test_pickle = model.JsonProperty()

        m = TestModel()
        self.assertEqual(m.test_pickle, None)
        m = TestModel(test_pickle={"123": "456"})
        self.assertEqual(m.test_pickle, {"123": "456"})

        m.test_pickle = {'456': '789'}
        self.assertEqual(m.test_pickle, {'456': '789'})


    def testDataTimeProperty(self):
        import datetime

        class TestModel(model.Model):
            test_datetime = model.DateTimeProperty()

        m = TestModel()
        self.assertEqual(m.test_datetime, None)

        utcnow = datetime.datetime.utcnow()
        m.test_datetime = utcnow
        self.assertEqual(m.test_datetime, utcnow)


    def testDateProperty(self):
        import datetime

        class TestModel(model.Model):
            test_date = model.DateProperty()

        m = TestModel()
        self.assertEqual(m.test_date, None)

        today = datetime.date.today()
        m.test_date = today
        self.assertEqual(m.test_date, today)

    def testTimeProperty(self):
        import datetime

        class TestModel(model.Model):
            test_time = model.TimeProperty()

        m = TestModel()
        self.assertEqual(m.test_time, None)

        t = datetime.time()
        m.test_time = t

        self.assertEqual(m.test_time, t)

    def testInsert(self):
        class TestModel(model.Model):
            test_value = model.StringProperty()

        conn = Connection()
        http = conn._http = Http({'status': '200'}, '')
        datastore.set_default_connection(conn)
        entity = TestModel(id=1)
        entity.test_value = '123'
        entity.put()

        self.assertEqual(entity['test_value'], '123')
        # self.assertEqual(connection._saved,
        #                  (_DATASET_ID, 'KEY', {'test_value': '123'}, ()))
        # self.assertEqual(key._path, None)


class Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content

