import tkinter as tk
import getData
import json
import os
from tabulate import tabulate
import schedule
import time
class classRefresher():
    
    filename = "vt_api\\dataObjects.json"
    
    def __init__(self, fileList) -> None:
        schedule.every(5).seconds.do(lambda : print("hi"))

    

