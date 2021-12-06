import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime

class Parser(object):
  def __init__(self):
    ints = Word(nums)

    # timestamp
    month = Word(string.ascii_uppercase , string.ascii_lowercase, exact=3)
    day   = ints
    hour  = Combine(ints + ":" + ints + ":" + ints)
    
    timestamp = month + day + hour

    # service_name
    service_name = Word(alphas + nums + "_" + "-" + ".")

    # appname
    appname = Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")

    # message
    message = Regex(".*")
  
    # pattern build
    self.__pattern = timestamp + hostname + appname + message
    
  def parse(self, line):
    parsed = self.__pattern.parseString(line)

    payload              = {}
    payload["timestamp"] = strftime("%Y-%m-%d %H:%M:%S")
    payload["hostname"]  = parsed[4]
    payload["appname"]   = parsed[5]
    payload["pid"]       = parsed[6]
    try:
        payload["message"]   = parsed[7]
    except IndexError:
        payload["message"] = ''
    return payload

