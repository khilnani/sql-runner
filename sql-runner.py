#!/usr/bin/env python

######################################################################
#
#    sql-runner.py
#    Copyright (C) 2014  Nik Khilnani   nik@Khilnani.org
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#######################################################################

import sys
import os
import json


##################################################
# Color class
##################################################

class Color:
  BLACK   = '\033[90m'
  RED     = '\033[91m'
  GREEN   = '\033[92m'
  YELLOW  = '\033[93m'
  BLUE    = '\033[94m'
  MAGENTA = '\033[95m'
  CYAN    = '\033[96m'
  WHITE   = '\033[97m'
  END = '\033[0m'

  @staticmethod
  def black( msg ):
      print Color.BLACK + msg + Color.END

  @staticmethod
  def red( msg ):
      print Color.RED + msg + Color.END

  @staticmethod
  def green( msg ):
      print Color.GREEN + msg + Color.END

  @staticmethod
  def yellow( msg ):
      print Color.YELLOW + msg + Color.END

  @staticmethod
  def blue( msg ):
      print Color.BLUE + msg + Color.END

  @staticmethod
  def magenta( msg ):
      print Color.MAGENTA + msg + Color.END

  @staticmethod
  def cyan( msg ):
      print Color.CYAN + msg + Color.END

  @staticmethod
  def white( msg ):
      print Color.WHITE + msg + Color.END

##################################################
# App
##################################################

# Check if library is installed
try:
  import pymysql
except:
  Color.red("Please install pymysql: pip install pymysql")
  sys.exit()

# Run SQL for a connection
def exec_sql(conn, params, sqls):
  Color.yellow("DB: {}".format( conn["id"] ))
  Color.green( "Params: " + str(params) )
  # Connect to db
  db = pymysql.connect( conn["url"], conn["username"], conn["password"], conn["db"] )
  # Iterate through each SQL
  for sql in sqls:
    Color.magenta("  SQL: {}".format( sql["id"] ))
    # substitute params
    query = sql["sql"]
    for param in params:
      query = query.replace(param, params[param])
    # Execute sql
    cursor = db.cursor()
    cursor.execute( query )
    results = cursor.fetchall()
    # Print each row in the result set
    for row in results:
      print "    {}".format(str(row))
  db.close()

# Main driver
def run(json_file):
  try:
    # load json
    db_json = open(json_file, "r")
    # Parse the json
    db_config = json.load(db_json)
    # CLose file
    db_json.close()
    # Iterate through each connection set
    for item in db_config:
      # Run the sql for each conection
      for conn in item["conns"]:
        exec_sql( conn, item["params"], item["sqls"] )
  except Exception as e:
    Color.red(str(e))
    sys.exit()

##################################################
# Main
##################################################


if __name__ == "__main__":
  if len(sys.argv) == 2:
    json_file = sys.argv[1]
    Color.blue( "JSON: {}".format( json_file ) )
    run( json_file )
  else:
    Color.red( "USAGE: {} JSON".format(sys.argv[0]) )
