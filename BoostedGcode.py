# Copyright (c) 2018 Csaba Garay, www.customize-3d.com
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.
from ..Script import Script

import urllib
import json
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from UM.Logger import Logger

class BoostedGcode(Script):
  def __init__(self):
    super().__init__()

  def getSettingDataString(self):
    settings = ""
    try:
      config_url = 'http://us-central1-boosted-gcode.cloudfunctions.net/cura-post-process-plugin-script-config'
      headers = {}
      headers['Content-type'] = 'application/json'
      values = {}
      values['cura_version'] = "3.2.1"
      data = urlencode(values).encode('ascii')
      req = Request(config_url, data=data, method='POST')
      resp = urlopen(req)
      if resp.getcode() == 200:
        settings = resp.read().decode('ascii')
      else:
        error_msg = "Could not fetch script config from internet"
        Logger.log("d", error_msg)
        raise Exception(error_msg)
    except:
      # Default setting if config couldn't be fetched
      # TODO better exception handling checking
      settings =  """{
          "name":"Boosted Gcode",
          "key": "BoostedGcode",
	  "metadata": {},
	  "version": 2,
	  "settings":
	  {
	    "activation_code":
	    {
	      "label": "Activation code",
	      "description": "None",
	      "type": "int",
	      "default_value": "1111111111111111"
	    },
	    "nozzle_size":
	    {
	      "label": "Nozzle diameter",
	      "description": "Nozzle diameter in mm",
	      "unit": "mm",
	      "type": "float",
	      "default_value": 0.4,
	      "minimum_value": "0",
	      "minimum_value_warning": "0.1",
	      "maximum_value_warning": "2"
	    },
      "retraction_distance":
      {
      "label": "Retraction distance",
      "description": "Retraction distance in mm",
        "unit": "mm",
        "type": "float",
        "default_value": 4.5,
        "minimum_value": "0",
        "maximum_value_warning": "30"
      },
      "layer_height":
      {
        "label": "Layer height",
        "description": "Layer height",
        "unit": "mm",
        "type": "float",
        "default_value": 0.1,
        "minimum_value": "0.01",
        "maximum_value_warning": "30.0"
      },
      "z_merge_number":
      {
        "label": "Z-Merge number",
        "description": "How many layers of infill are z-merged",
        "unit": "",
        "type": "int",
        "default_value": 4,
        "minimum_value": "0",
        "maximum_value_warning": "30"
      },
	    "boosted_gcode_cloud_func_url":
	    {
	      "label": "Cloud function URL",
	      "description": "Don't change",
	      "type": "str",
	      "default_value": "http://us-central1-boosted-gcode.cloudfunctions.net/z-merge-infill2"
	    }
         }
      }"""

    Logger.log("d", "Settings: %s" % settings)
    return settings


  def execute(self, data):
    gcode = '\n'.join(data)

    url = str(self.getSettingValueByKey('boosted_gcode_cloud_func_url'))
    Logger.log("d", "URL to connect: %s" % url)

    headers = {}
    headers['Content-type'] = 'application/json'
    values = {}
    values['activation_code'] = str(self.getSettingValueByKey('activation_code'))
    values['nozzle_size'] = str(self.getSettingValueByKey('nozzle_size'))
    values['retraction_distance'] = str(self.getSettingValueByKey('retraction_distance'))
    values['layer_height'] = str(self.getSettingValueByKey('layer_height'))
    values['z_merge_number'] = str(self.getSettingValueByKey('z_merge_number'))

    Logger.log("d", "Number of lines to be uploaded: %s" % len(data))
    values['content'] = gcode

    data = urlencode(values).encode('ascii')

    req = Request(url, data=data, method='POST')

    Logger.log("d", "Connecting to server...")
    resp = urlopen(req)
    Logger.log("d", "Connection complete, response code is: %d" % resp.getcode())

    Logger.log("d", "Reading content...")
    modified_content = resp.readlines()
    Logger.log("d", "Reading complete.")

    Logger.log("d", "Decoding content...")
    new_gcode = []
    for l in modified_content:
      new_gcode += l.decode('ascii')
    Logger.log("d", "Decoding complete.")

    Logger.log("d", "Content read complete. Number of lines received: %d" % len(modified_content))


    modified_gcode = []
    modified_gcode += [";Modified by Boosted Gcode post processing - more info at customize-3d.com\n"]
    modified_gcode += new_gcode

    return modified_gcode