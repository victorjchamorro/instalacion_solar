#!/usr/bin/python3
# *****Program to retrieve and store data to BMS PCBs*****
# Copyright (C) 2017 Simon Richard Matthews
# Project loaction https://github.com/simat/BatteryMonitor
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import bmscore
import sys
import binascii
import time, requests, json, urllib3, os
from urllib.parse import quote 

def getdat(port='/dev/ttyUSB0'):
  """ Get data from BMS board"""
  ser = bmscore.openbms(port)

  # status
  command = bytes.fromhex('DD A5 03 00 FF FD 77')
  dat = bmscore.getbmsdat(ser,command)
  rawi = int.from_bytes(dat[2:4], byteorder = 'big',signed=True)
  rawv = int.from_bytes(dat[0:2], byteorder = 'big',signed=True)
  balance = bin(int.from_bytes(dat[12:14], byteorder = 'big',signed=True))
  state = int.from_bytes(dat[16:18], byteorder = 'big',signed=True)
  fets = bin(int.from_bytes(dat[20:21], byteorder = 'big',signed=True))
  
  print ("V={} I={} bal={} state={} fets={}".format(rawv,rawi,balance,bin(state),fets))
  errors=['Cell Overvoltage','Cell Undervoltage','Battery Overvoltage', \
          'Battery Undervoltage','Charge Overtemp','Charge Undertemp', \
          'Discharge Overtemp','Discharge Undertemp','Charge Overcurrent' \
          'Discharge Overcurrent','Short Circuit','IC Fault','Software MOS lock']
  for i in range(state.bit_length()):
    if 2**i & state:
      print (errors[i])

  # voltages
  command = bytes.fromhex('DD A5 04 00 FF FC 77')
  voltages = bmscore.getbmsdat(ser,command)
  ser.close
  #print (binascii.hexlify(voltages))
  rawv = [ 0 for i in range(19)]
  rawb = [ 0 for i in range(15)]
  rawt = {}

  total = 0
  mini=0
  maxi=0
  
  for i in range(15):
    rawv[i] = int.from_bytes(voltages[i*2:i*2+2], byteorder = 'big')#/1000.00
    #Suma
    total += rawv[i]
    
    #Serie minima
    if (mini==0):
        mini=rawv[i]
    else:
        if (rawv[i] < mini): 
            mini=rawv[i]
            
    #Serie maxima
    if (rawv[i] > maxi):
        maxi=rawv[i]
    
    if (i == 0):
        rawb[i] = int.from_bytes(dat[12:14], byteorder = 'big',signed=True) & 1
    else:
        rawb[i] = int.from_bytes(dat[12:14], byteorder = 'big',signed=True) >> i & 1

  # temperaturas

  for i in range(int.from_bytes(dat[22:23],'big')): # read temperatures
    rawt['T{0:0=1}'.format(i+1)]=(int.from_bytes(dat[23+i*2:i*2+25],'big')-2731)/10
        
  rawv[15] = total;
  rawv[16] = mini;
  rawv[17] = maxi;
  rawv[18] = maxi - mini;
  
  print (rawv)
  print (rawb)
  print (rawt)
  
  emoncms(rawv,rawb,rawt)

def main():  
	port='/dev/ttyUSB_bms'    
	while True:
		try:
			bmscore.openbms(port)
			getdat(port)
			time.sleep(5)
		except:
			print('Error de conexion con el bms')
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print(sys.exc_info())
			time.sleep(4)
      
def emoncms(res,balance,temperaturas):
	
	if (float(res[15])==0):
		print("empty")
		return;
	
	apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	
	data={
		"s1":  res[14],
		"s2":  res[13],	
		"s3":  res[12],
		"s4":  res[11],
		"s5":  res[10],
		"s6":  res[9],
		"s7":  res[8],
		"s8":  res[7],
		"s9":  res[6],
		"s10": res[5],
		"s11": res[4],
		"s12": res[3],
		"s13": res[2],
		"s14": res[1],
		"s15": res[0],
		"V":   res[15],
		"min": res[16],
		"max": res[17],
		"diff":res[18],
                "sb1": balance[14],
                "sb2": balance[13],
                "sb3": balance[12],
                "sb4": balance[11],
                "sb5": balance[10],
                "sb6": balance[9],
                "sb7": balance[8],
                "sb8": balance[7],
                "sb9": balance[6],
                "sb10":balance[5],
                "sb11":balance[4],
                "sb12":balance[3],
                "sb13":balance[2],
                "sb14":balance[1],
                "sb15":balance[0],
                "t1":temperaturas['T1'],
                "t2":temperaturas['T2']
	}
	
	y= json.dumps(data)

	url="http://localhost/emoncms/input/post?node=bms&fulljson="+quote(y)+"&apikey="+apikey 
	print(url)
	
	r=requests.get(url);
	print(r.content)
	

if __name__ == "__main__":
  """if run from command line"""
  main()
