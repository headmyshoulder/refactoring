#! /usr/bin/python

""" rename_includes.py """
 
__date__ = "2015-12-15"
__author__ = "Karsten Ahnert"
__email__ = "karsten.ahnert@gmx.de"

import sys
import argparse
import logging
import os

def parseCmd( argv ):
    parser = argparse.ArgumentParser( description = "Application description" )
    parser.add_argument( "input" , type=str )
    args = parser.parse_args( argv[1:] )
    return args

def initLogging( args ):
    formatString = '[%(levelname)s][%(asctime)s] : %(message)s'
    logLevel = logging.INFO
    logging.basicConfig( format=formatString , level=logLevel , datefmt='%Y-%m-%d %I:%M:%S')

def main( argv ):

    args = parseCmd( argv )
    initLogging( args )
    
    logging.info( "Processing directory " + args.input )
    for subdir, dirs, files in os.walk( args.input ):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith( ".hpp" ) or filepath.endswith( ".cpp" ):
                with open( filepath , "r" ) as f:
                    new = ""
                    for line in f.readlines():
                        prefix = "#include <formula"
                        if line.startswith( prefix ):
                            new += "#include <formula/core" + line[ len( prefix ) : ]
                        else:
                            new += line
                    logging.info( "Processing source file " + filepath )
                with open( filepath , "w" ) as f:
                    f.write( new )
                        
                        

if __name__ == "__main__" :
    main( sys.argv )

