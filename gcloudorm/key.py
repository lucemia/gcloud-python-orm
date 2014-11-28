from gcloud.datastore import key

class Key(key.Key):
    def __init__(self, *args, **kwargs):
        app = kwargs.get("app")
        namespace = kwargs.get("namespace")
        pairs = kwargs.get("pairs")
        flat = kwargs.get("flat")
        urlsafe = kwargs.get("urlsafe")
        path = kwargs.get("path")

        if urlsafe:
            raise NotImplementedError()

        if not path:
            if not pairs:
                if not flat:
                    flat = args

                assert len(flat) % 2 == 0
                pairs = [(flat[i], flat[i+1]) for i in range(0, len(flat), 2)]

            path = []
            for kind, _id in pairs:
                if isinstance(_id, (int, long)):
                    path.append({'kind': kind, 'id': _id})
                elif isinstance(_id, basestring):
                    path.append({'kind': kind, 'name': _id})
                else:
                    raise SyntaxError("id should be either int or string")

        super(Key, self).__init__(path, namespace=namespace, dataset_id=app)

