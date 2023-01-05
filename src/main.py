# python libraries
import time
from typing import Optional
import uuid
import os

# Installed libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# custom modules
from configs.config import settings

from src.constants import Constants

from src.routers import checks, slice, filter, yolov5, tiny_object_inference, coco_ops

def get_app() -> FastAPI:
  try:
      fast_app = FastAPI(title=settings.app_name)
      return fast_app
  except Exception as e:
      print(f'exception occured in get_app() - {e}')

app = get_app()

app.include_router(checks.router)
app.include_router(slice.router)
app.include_router(filter.router)
app.include_router(coco_ops.router)
app.include_router(yolov5.router)
app.include_router(tiny_object_inference.router)
