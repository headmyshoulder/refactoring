#! /usr/bin/python

""" remove_header_guards.py """
 
__date__ = "2015-12-15"
__author__ = "Karsten Ahnert"
__email__ = "karsten.ahnert@gmx.de"

import sys
import argparse
import logging

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
                    logging.info( "Processing source file " + filepath )
                    lines = []
                    found = False
                    for line in f.readlines():
                        lines.append( line )
                    newlines = ""
                    for i in range( 1 , len( lines ) ):
                        l1 = lines[i-1]
                        l2 = lines[i]
                        if l1.startswith( "#ifndef " ) and l1.startswith( "#define" ) and l1.contains( "INCLUDED" ) and l2.contains( "INCLUDED" ):
                            newlines.append( "#pragma once\n" )
                            found = True
                        else:
                            newlines.append( l1 )
                    newlines.append( lines[-1] )
                    
                    if found:
                        
                    
                            
                with open( filepath , "w" ) as f:
                    f.write( new )

if __name__ == "__main__" :
    main( sys.argv )

