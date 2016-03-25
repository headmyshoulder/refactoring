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
    parser.add_argument( "input" , type=str , help="Input directory" )
    parser.add_argument( "--dry" , dest='dry' , help="Dry run without modification" , action='store_true' )
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
    if args.dry:
        logging.info( "Dry run without modification" )
    for subdir, dirs, files in os.walk( args.input ):
        for file in files:
            filepath = subdir + os.sep + file
            # if filepath.endswith( ".hpp" ) or filepath.endswith( ".cpp" ) or filepath.endswith( ".h" ):
            if filepath.endswith( ".cpp" ):
                with open( filepath , "r" ) as f:
                    new = ""
                    changed = False                    
                    for line in f.readlines():
                        
                        searchString = "ETCStateMachine"
                        if searchString in line:
                            changed = True
                            new += line.replace( searchString , "SegmentMautStateMachine" )
                            logging.info( "Found occurence in " + filepath )
                        
                        # prefix = "#include <formula"
                        # if line.startswith( prefix ):
                        #    new += "#include <formula/core" + line[ len( prefix ) : ]
                        
                        else:
                            new += line
                    logging.info( "Processing source file " + filepath )
                if not args.dry and changed:
                    with open( filepath , "w" ) as f:
                        f.write( new )
                        
                        

if __name__ == "__main__" :
    main( sys.argv )

