from models.modelLog import database as db
import lasio

db = db()

def search_wellInfo():
  try:
    data_list = []
    for data in db.show_wellInfo():
      data["_id"] = str(data["_id"])
      data_list.append(data)
    return data_list
  except Exception as e:
    return {"error": str(e)}

def search_wellInfo_by_file(**params):
  try:
    data_list = []
    for data in db.show_wellInfoByFile(**params):
      data["_id"] = str(data["_id"])
      data_list.append(data)
      return data_list
  except Exception as e:
    return {"error": str(e)}

def delete_wellInfo_by_file_mnemonic(**params):
  try:
    db.delete_wellInfoByFileMnemonic(**params)
    return {"success": "Data has been deleted"}
  except Exception as e:
    return {"error": str(e)}

def update_wellInfo_by_file_mnemonic(**params):
  try:
    result = db.update_wellInfoByFileMnemonic(**params)
    result["_id"] = str(result["_id"])
    return {
      "success": "Data has been updated",
      "updated-data": result}
  except Exception as e:
    return {"error": str(e)}

def search_logInfo():
  try:
    data_list = []
    for data in db.show_logInfo():
      data["_id"] = str(data["_id"])
      data_list.append(data)
    return data_list
  except Exception as e:
    return {"error": str(e)}

def search_logInfo_by_file(**params):
  try:
    data_list = []
    for data in db.show_logInfoByFile(**params):
      data["_id"] = str(data["_id"])
      data_list.append(data)
    return data_list
  except Exception as e:
    return {"error": str(e)}

def delete_logInfo_by_file_mnemonic(**params):
  try:
    db.delete_logInfoByFileMnemonic(**params)
    return {"success": "Data has been deleted"}
  except Exception as e:
    return {"error": str(e)}

def update_logInfo_by_file_mnemonic(**params):
  try:
    result = db.update_logInfoByFileMnemonic(**params)
    result["_id"] = str(result["_id"])
    return {
      "success": "Data has been updated",
      "updated-data": result}
  except Exception as e:
    return {"error": str(e)}

def search_logData():
  try:
    data_list = []
    for data in db.show_logData():
      data["_id"] = str(data["_id"])
      data["data"] = str(data["data"])
      data_list.append(data)
    return data_list
  except Exception as e:
    return {"error": str(e)}

def search_logData_by_file(**params):
  try:
    data_list = []
    for data in db.show_logDataByFile(**params):
      data["_id"] = str(data["_id"])
      data["data"] = str(data["data"])
      data_list.append(data)
    return data_list
  except Exception as e:
    return {"error": str(e)}

def insertLAS(document):
  try:
    #path = f"\fileLAS\{document}"
    las = lasio.read(document)
    wellData = [{
      "filename": document,
      "mnemonic": well.mnemonic,
      "desc": well.descr,
      "unit": well.unit,
      "value": well.value}
      for well in las.well]

    curveData = [{
      "filename": document,
      "API_code": curve.value,
      "mnemonic": curve.mnemonic,
      "desc": curve.descr,
      "unit": curve.unit,
      "data_shape": curve.data.shape}
      for curve in las.curves]

    log_titles = [curve.mnemonic for curve in las.curves]
    data = dict()
    logData = [{
      "filename": document,
      "version": las.version[0].descr,
      "data" : data
    }]
    for n in range(len(las.data)):
      id_ = str(n)
      log_values = las.data[n]
      log_data =  dict(zip(log_titles, log_values))
      data[id_]=log_data
    
    params = {
      "well-information": wellData,
      "log-information": curveData,
      "log-data": logData
    }
    db.insert_Data(**params)
    return {"success": "Data has been inserted"}
  
  except Exception as e:
    print(e)
    return {"error": str(e)}
