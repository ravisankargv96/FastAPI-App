from pymongo import MongoClient

class database:
  def __init__(self):
    try:
      self.nosql_db = MongoClient()
      self.db = self.nosql_db.wellLog
      self.wellInfo = self.db.wellInformation
      self.logInfo = self.db.logInformation
      self.logData = self.db.logData
    except Exception as e:
      print(e)

  def show_wellInfo(self):
    result = self.wellInfo.find()
    return [item for item in result]

  def show_wellInfoByFile(self, **params):
    result = self.wellInfo.find({"filename":params["filename"]})
    return [item for item in result]

  def update_wellInfoByFileMnemonic(self, **params):
    query_1 = {
      "filename":params["filename"],
      "mnemonic":params["mnemonic"]}
    query_2 = {"$set": params["update"]}
    self.wellInfo.update_one(query_1, query_2)
    return self.wellInfo.find_one(query_1)

  def delete_wellInfoByFileMnemonic(self, **params):
    self.wellInfo.delete_one({
      "filename":params["filename"],
      "mnemonic":params["mnemonic"]})

  def show_logInfo(self):
    result = self.logInfo.find()
    return [item for item in result]
  
  def show_logInfoByFile(self, **params):
    result = self.logInfo.find({"filename":params["filename"]})
    return [item for item in result]

  def update_logInfoByFileMnemonic(self, **params):
    query_1 = {
      "filename":params["filename"],
      "mnemonic":params["mnemonic"]}
    query_2 = {"$set": params["update"]}
    self.logInfo.update_one(query_1, query_2)
    return self.logInfo.find_one(query_1)

  def delete_logInfoByFileMnemonic(self, **params):
    self.logInfo.delete_one({
      "filename":params["filename"],
      "mnemonic":params["mnemonic"]})

  def show_logData(self):
    result = self.logData.find()
    return [item for item in result]

  def show_logDataByFile(self, **params):
    result = self.logData.find({"filename":params["filename"]})
    return [item for item in result]

  def insert_Data(self, **params):
    self.wellInfo.insert_many(params["well-information"])
    self.logInfo.insert_many(params["log-information"])
    self.logData.insert_many(params["log-data"])
