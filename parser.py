import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from datetime import datetime, date
import re

class Parser(object):
  def __init__(self):
    ints = Word(nums)
  
    # timestamp
    month = Word(string.ascii_uppercase , string.ascii_lowercase, exact=3)
    day   = ints
    time_collect  = Combine(ints + ":" + ints + ":" + ints)
    
    timestamp = month + day + time_collect

    # hostname
    hostname = Word(alphas + nums + "_" + "-" + ".")

    # appname
    appname = Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")

    # message
    message = Regex(".*")
  
    # pattern build
    self.__pattern = timestamp + hostname + appname + message
    
  def parse(self, line):
    parsed = self.__pattern.parseString(line)

    
    payload = {}
    payload["timestamp"] = parsed[2] + parsed[1] + "//" + str(datetime.strptime(parsed[0], "%b").month) + "//" + str(date.today().year)
    payload["hostname"]  = parsed[3]
    payload["appname"]   = parsed[4]

    if len(parsed) == 7:      
      payload["pid"]       = parsed[5]
      payload["message"]   = parsed[6]
    elif len(parsed) == 6:
      proccess_parsed_text = parsed[5].replace(re.findall("\[.*?\]", parsed[5])[0] + " ", '') # remove extra content from it
      list_of_variables = proccess_parsed_text.split(" ")
      
      for a_variable in list_of_variables:
        if '=' in a_variable:
          list_from_a_variable = a_variable.split("=")
          payload[list_from_a_variable[0]] = '='.join (map(str, list_from_a_variable[1:]))
        elif ':' in a_variable:
          list_from_a_variable = a_variable.split(":")
          payload[list_from_a_variable[0]] = ':'.join (map(str, list_from_a_variable[1:]))


      
    else:
      raise Exception("Need to handle this log")
      
    return payload