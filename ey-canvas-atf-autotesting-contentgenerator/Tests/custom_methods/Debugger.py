import os
import datetime
from scriptless.Core.library.common.CustomBase import CustomBase

class Debugger(CustomBase):
    
    def break_point(self,var = None):
        print("Debugger...")
        print(var)