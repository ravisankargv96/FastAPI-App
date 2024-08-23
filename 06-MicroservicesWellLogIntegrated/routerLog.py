from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi import APIRouter, File, UploadFile
from apiLog import *
import os, shutil

router = APIRouter()

@router.post("/upload-las/")
async def upload_las(las: UploadFile = File(...)):
  try:
    os.chdir("fileLAS")
    file_name = las.filename.replace(" ","-")
    with open(file_name,'wb+') as output_file:
      shutil.copyfileobj(las.file, output_file)
      # content = las.file.read()
      # output_file.write(content)

    result = insertLAS(file_name)
    return result
    
  except Exception as e:
    return {"error": str(e)}


@router.get("/well-information")
async def view_search_wellInfo():
  result = search_wellInfo()
  return result

@router.post("/well-information/search")
async def view_search_wellInfo_by_file(params:dict):
  result = search_wellInfo_by_file(**params)
  return result

@router.post("/well-information/delete")
async def execute_delete_wellInfo_by_file_mnemonic(params:dict):
  result = delete_wellInfo_by_file_mnemonic(**params)
  return result

@router.post("/well-information/update")
async def execute_update_wellInfo_by_file_mnemonic(params:dict):
  result = update_wellInfo_by_file_mnemonic(**params)
  return result

@router.get("/log-information")
async def view_search_logInfo():
  result = search_logInfo()
  return result

@router.post("/log-information/search")
async def view_search_logInfo_by_file(params:dict):
  result = search_logInfo_by_file(**params)
  return result

@router.post("/log-information/delete")
async def execute_delete_logInfo_by_file_mnemonic(params:dict):
  result = delete_logInfo_by_file_mnemonic(**params)
  return result

@router.post("/log-information/update")
async def execute_update_logInfo_by_file_mnemonic(params:dict):
  result = update_logInfo_by_file_mnemonic(**params)
  return result

@router.get("/log-data")
async def view_search_logData():
  result = search_logData()
  return result

@router.post("/log-data/search")
async def view_search_logData_by_file(params:dict):
  result = search_logData_by_file(**params)
  return result