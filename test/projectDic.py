#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  projectDic.py
#  
#  Copyright 2014 Labio <labio@labio-XPS-8300>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from pprint import pprint
dic= {

   'job_history'  :{
                 
                   # new propose
                   '1': {                                                      
                         'object'    : 'Step1'           ,
                         'type'      : 'new/min/dyn/prn' ,
                         'parameters': 'parameters'      ,      # -  extracted from the log -  checksystem
                         'potencial' : "AMBER/AM1/ABFS"  ,
                         'CQatoms'   : '43'              ,
                         'color'     : 'black'
                        }
                   }
    }




def main():
	#pprint(dic)
    print dic['job_history']['1']['object']
    return 0

if __name__ == '__main__':
	main()

