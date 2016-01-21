#! /usr/bin/python

""" remove_header_guards.py """


__date__ = "2015-12-15"
__author__ = "Karsten Ahnert"
__email__ = "karsten.ahnert@gmx.de"


import sys
import argparse
import logging
import os

def parse_cmd( argv ):
    parser = argparse.ArgumentParser( description = "Application description" )
    parser.add_argument( "input" , type=str , help="Input directory" )
    parser.add_argument( "--dry" , dest='dry' , help="Dry run without modification" , action='store_true' )
    args = parser.parse_args( argv[1:] )
    return args

def init_logging( args ):
    formatString = '[%(levelname)s][%(asctime)s] : %(message)s'

    logLevel = logging.INFO
    logging.basicConfig( format=formatString , level=logLevel , datefmt='%Y-%m-%d %I:%M:%S')
    
    
def find_line( lines , string ):
    result = []
    count = 0
    for line in lines:
        if line.startswith( string ):
            result.append( count )
        count += 1
    return result

def main( argv ):
    
    args = parse_cmd( argv )
    init_logging( args )
    
    logging.info( "Processing directory " + args.input )
    if args.dry:
        logging.info( "Dry run without modification" )
    for subdir, dirs, files in os.walk( args.input ):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith( ".hpp" ) or filepath.endswith( ".h" ):
                with open( filepath , "r" ) as f:
                    lines = []
                    for line in f.readlines():
                        lines.append( line )
                    
                    l1 = find_line( lines , "#ifndef" )
                    l2 = find_line( lines , "#define" )
                    l3 = find_line( lines , "#endif" )
                    
                    if ( len( l1 ) == 1 ) and ( len( l2 ) == 1 ) and ( len( l3 ) == 1 ) :
                        l1 = l1[0]
                        l2 = l2[0]
                        l3 = l3[0]
                        if ( abs( len( lines ) - l3 ) < 2 ) and ( l2 == ( l1 + 1 ) ) and ( l1 < 20 ):
                            logging.info( filepath + " : changing header guards." )
                            newlines = lines[:l1]
                            newlines.append( "#pragma once\n" )
                            newlines.extend( lines[l2+1:l3] )
                            newlines.extend( lines[l3+1:] )
                            if not args.dry:
                                with open( filepath , "w" ) as f:
                                    for line in newlines:
                                        f.write( line )
                        else:
                            logging.info( filepath + " position of #ifndef, #defines, #endifs is strange." )
                    else:
                        l4 = find_line( lines , "#pragma once" )
                        if len( l4 ) != 1:
                            logging.info( filepath + " looks strange: " + str( l1 ) + " , " + str( l2 ) + " , " + str( l3 ) )
                   
                        
                #with open( filepath , "w" ) as f:
                    #f.write( new )

if __name__ == "__main__" :
    main( sys.argv )

