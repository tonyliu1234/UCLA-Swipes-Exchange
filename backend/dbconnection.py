from pymongo import MongoClient

class DBConnection:
    def __init__(self, host='localhost', port=27017, db_name='mydatabase'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """Create a MongoDB connection and return the database instance."""
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        return self.db

    def get_collection(self, collection_name):
        """Get a collection from the connected database."""
        if self.db is None:
            raise Exception('Database not connected. Call the connect() method first.')
        return self.db[collection_name]

class DBOperations:
  def __init__(self, db_connection, collection_name):
    self.db_connection = db_connection
    self.collection_name = collection_name

  def create(self, data):
    collection = self.db_connection.get_collection(self.collection_name)
    result = collection.insert_one(data)
    return result.inserted_id

  def get(self, document_id):
    collection = self.db_connection.get_collection(self.collection_name)
    return collection.find_one({'_id': document_id})

  def update(self, document_id, update_data):
    collection = self.db_connection.get_collection(self.collection_name)
    result = collection.update_one(
        {'_id': document_id},
        {'$set': update_data}
    )
    return result.modified_count

  def delete(self, document_id):
    collection = self.db_connection.get_collection(self.collection_name)
    result = collection.delete_one({'_id': document_id})
    return result.deleted_count
