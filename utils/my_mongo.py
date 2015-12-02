from pymongo import MongoClient
# import pandas as pd
__author__ = 'sunary'


class Mongodb:

    def __init__(self, host='localhost', port=27017, db=None, col=None):
        self._client = MongoClient(host, port)
        self._db = self._client[db]
        self.host = host
        self.name_db = db
        self.name_col = col
        self.collection = self._db[col]

    def find(self, spec={}, select=[], limit=0, skip=0, chunk_size=500, sort=None, **kwargs):
        if limit:
            cur = self.collection.find(
                    filter=spec,
                    projection=select,
                    skip=skip,
                    limit=limit,
                    **kwargs
                )

            if sort:
                cur = cur.sort(sort)

            for each in cur:
                yield each
        else:
            while True:
                cur = self.collection.find(
                    filter=spec,
                    projection=select,
                    skip=skip,
                    limit=chunk_size,
                    **kwargs
                )
                if sort:
                    cur = cur.sort(sort)

                if cur.count(True) == 0:
                    break
                for each in cur:
                    yield each
                    skip += 1

    def find_one(self, spec=None, **kwargs):
        return self.collection.find_one(spec, **kwargs)

    def insert(self, docs, **kwargs):
        return self.collection.insert(doc_or_docs=docs, **kwargs)

    def update(self, spec, doc, **kwargs):
        if doc.get('$set'):
            return self.collection.update(spec, doc, **kwargs)
        return self.collection.update(spec, {'$set': doc}, **kwargs)

    def batch_update(self, spec, docs, **kwargs):
        bulk = self.collection.initialize_unordered_bulk_op()
        for i in range(len(docs)):
            bulk.find(spec[i]).update({'$set': docs[i]})

        bulk.execute()

    def increase(self, spec, doc, **kwargs):
        if doc.get('$inc'):
            return self.collection.update(spec, doc, **kwargs)
        return self.collection.update(spec, {'$inc': doc}, **kwargs)

    def count(self, spec=None):
        return self.collection.find(spec).count()

    def remove(self, spec=None):
        if spec is None:
            self.collection.remove()
        else:
            self.collection.remove(spec=spec)

    def create_index(self, keys, **kwargs):
        self.collection.create_index(keys, **kwargs)

    def export_csv(self, fields, output):
        from utils import my_helper

        logger = my_helper.init_logger(self.__class__.__name__)
        command = 'mongoexport -h %s -d %s -c %s -f %s --csv -o %s' % (self.host, self.name_db, self.name_col, ','.join(fields), output)
        logger.info(command)
        output_str = my_helper.subprocess_output(command)

        logger.info(output_str)

    def export_excel(self, fields, output):
        result = []
        for doc in self.find(select=fields):
            result.append(doc)
        df = pd.DataFrame(data=result, columns=fields)
        df.to_excel(output, index=False, encoding='utf-8')
