import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from datetime import datetime, date
import re


def clean_string(input):
  if isinstance(input, int):
    return input
  elif isinstance(input, str):
    return input.replace('"', '').replace("'", "").strip()
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
    payload['log'] = {}
    payload["time"] = parsed[2] + parsed[1] + "/" + str(datetime.strptime(parsed[0], "%b").month) + "/" + str(date.today().year)
    payload["time"] = payload["time"].replace("//", "/")
    payload["hostname"]  = clean_string(parsed[3])
    payload['log']["Application"]   = clean_string(parsed[4])
    payload['logType'] = 'syslog'
    payload['logName'] = 'syslog'
    payload['siteName'] = ''
    if len(parsed) == 7:      
      payload['log']["pid"]       = clean_string(parsed[5])
      payload['log']["message"]   = clean_string(parsed[6])
    elif len(parsed) == 6:
      proccess_parsed_text = parsed[5].replace(re.findall("\[.*?\]", parsed[5])[0] + " ", '') # remove extra content from it
      list_of_variables = proccess_parsed_text.split(" ")
      
      for a_variable in list_of_variables:
        if '=' in a_variable:
          list_from_a_variable = a_variable.split("=")
          if '(' in list_from_a_variable[0]:
            continue
          if len(list_from_a_variable) < 2:
            continue
          payload['log'][list_from_a_variable[0]] = clean_string('='.join (map(str, list_from_a_variable[1:])))
        elif ':' in a_variable:
          list_from_a_variable = a_variable.split(":")
          if '(' in list_from_a_variable[0]:
            continue
          if len(list_from_a_variable) < 2:
            continue
          payload['log'][list_from_a_variable[0]] = clean_string(':'.join (map(str, list_from_a_variable[1:])))
    else:
      raise Exception("Need to handle this log")  
    return payload