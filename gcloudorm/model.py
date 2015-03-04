from gcloud import datastore
from gcloud.datastore import entity, key
from .property import *

class MetaModel(type):
    def __init__(cls, name, bases, classdict):
        super(MetaModel, cls).__init__(name, bases, classdict)
        cls._fix_up_properties()


class Model(entity.Entity):
    __metaclass__ = MetaModel

    # name, prop dict
    _properties = None
    _kind_map = {}

    _model_exclude_from_indexes = None

    def __init__(self, id=None, parent=None, **kwargs):
        super(Model, self).__init__(exclude_from_indexes=self._model_exclude_from_indexes)

        if isinstance(parent, key.Key):
            flat = []
            for k in parent.path:
                flat.extend([k["kind"], k.get("id") or k.get("name")])

            if id is None:
                flat.extend([self.__class__.__name__])
            else:
                flat.extend([self.__class__.__name__, id])

            self._key = key.Key(*flat)
        else:
            if id is None:
                self._key = key.Key(self.__class__.__name__)
            elif isinstance(id, (int, long, basestring)):
                self._key = key.Key(self.__class__.__name__, id)
            else:
                raise SyntaxError()

        for attr in self._properties:
            setattr(self, attr, getattr(self, attr))

        for name in kwargs:
            setattr(self, name, kwargs[name])

    @property
    def key(self):
        return self._key
    @key.setter
    def key(self, value):
        self._key = value


    @classmethod
    def _fix_up_properties(cls):
        cls._properties = {}
        cls._model_exclude_from_indexes = set()

        for name in cls.__dict__:
            attr = cls.__dict__[name]
            if isinstance(attr, Property):
                attr._fix_up(cls, name)
                cls._properties[attr._name] = attr
                if attr._indexed == False:
                    cls._model_exclude_from_indexes.add(attr._name)

        cls._kind_map[cls.__name__] = cls

    @classmethod
    def _lookup_model(cls, kind):
        return cls._kind_map[kind]

    def __repr__(self):
        if self._key:
            return "<%s%s %s>" % (
                self.__class__.__name__,
                self._key.path(),
                super(Model, self).__repr__()
            )
        else:
            return "<%s %s>" % (
                self.__class__.__name__,
                super(Model, self).__repr__()
            )

    @classmethod
    def from_entity(cls, entity):
        obj = cls()
        obj._key = entity.key

        for name in cls._properties:
            value = entity.get(name)
            # string property from protobuf is str, but gcloud-python need unicode
            obj[name] = cls._properties[name].from_db_value(value)

        return obj

    @classmethod
    def get_by_id(cls, id):
        entity = datastore.get([key.Key(cls.__name__, id)])
        if entity:
            return cls.from_entity(entity[0])

    @classmethod
    def get_multi(cls, ids):
        entities = datastore.get([key.Key(cls.__name__, id) for id in ids])
        results = []

        for entity in entities:
            if entity is None:
                results.append(None)
            else:
                results.append(cls.from_entity(entity))

        return results

    def put(self, batch=None):
        for name, prop in self._properties.items():
            prop._prepare_for_put(self)

        if batch:
            return batch.put(self)
        else:
            return datastore.put([self])


def get_multi(keys):
    entities = datastore.get(keys)

    results = []
    for entity in entities:
        if entity is None:
            results.append(None)

        kind = entity.key().kind()

        model = Model._lookup_model(kind)
        results.append(model.from_entity(entity))

    return results
