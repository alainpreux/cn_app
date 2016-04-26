# -*- coding: utf-8 -*-

from __future__ import division
from datetime import datetime, timedelta
from io import open
import os
import shutil

import model
import logging


FOLDERS = ['Comprehension', 'Activite', 'ActiviteAvancee', 'cours', 'correction', 'webcontent']
VERBOSITY = False


def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 


def write_file(src, current_dir, target_folder, name):
    """
        given a "src" source string, write a file with "name" located in
        "current_dir"/"target_folder"
    """
    filename = os.path.join(current_dir, target_folder, name)
    try:
        outfile = open(filename, 'wb')
        outfile.write(src)
    except:
        logging.exception(" Error writing file %s" % filename)
        return False

    # if successful
    return True

def stitch_files(files, filename):
    with open(filename, "w", encoding='utf-8') as outfile:
        for f in files:
            with open(f, "r", encoding='utf-8') as infile:
                outfile.write(infile.read())
    return outfile
    
def createDirs(outDir):
    for folder in FOLDERS :
        new_folder = os.path.join(outDir, folder)
        # create and overwrite
        try:
            os.makedirs(new_folder)
        except OSError:
            # remove then create
            shutil.rmtree(new_folder, ignore_errors=True)
            os.makedirs(new_folder)
    
def processModule(module,repoDir,outDir=None, feedback_option=False):
    """ fetch markdown files from [repoDir]/[module]/ folder. 
        [repoDir] has to be given as absolute path. [module] is just the name of the module
        If no outDir given, build files directly in same folder, else in [repoDir]/[outDir]/[module]/
    """
    moduleDir = os.path.join(repoDir, module)
    if not outDir:
        outDir = moduleDir
    else:
        outDir = os.path.join(repoDir,outDir,module)

    # Fetch first md file in module folder
    filein = None
    for file in os.listdir(moduleDir):
        if '.md' in file:
            filein = os.path.join(moduleDir, file)
            break
    if not filein:
        logging.error(" No MarkDown file found, MarkDown file should end with '.md'")
        return false
    else:
        logging.info ("found MarkDown file : %s" % filein)
        

    # create folders
    createDirs(outDir)

    with open(filein, encoding='utf-8') as md_file:
        # parse md 
        m = model.Module(md_file, module)

    # write html,  XML, and JSon  files
    m.toHTMLFiles(outDir, feedback_option)
    m.toXMLMoodle(outDir)
    write_file(m.toGift(), outDir, '', module+'.questions_bank.gift.txt')
    write_file(m.toVideoList(), outDir, '', module+'.video_iframe_list.txt')
    write_file(m.toJson(), outDir, '',  module+'.config.json')
