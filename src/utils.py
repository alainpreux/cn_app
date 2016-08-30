# -*- coding: utf-8 -*-

from __future__ import division
from datetime import datetime, timedelta
from io import open
import os
import shutil

import model
import logging


FOLDERS = ['Comprehension', 'Activite', 'ActiviteAvancee', 'webcontent']
VERBOSITY = False
DEFAULT_VIDEO_THUMB_URL = 'https://i.vimeocdn.com/video/536038298_640.jpg'

def fetch_vimeo_thumb(video_link):
    """ fetch video thumbnail for vimeo videos """
    # get video id
    video_id = video_link.rsplit('/', 1)[1]
    logging.info ("== video ID = %s" % video_id)
    try: 
        response = requests.request('GET', VIDEO_THUMB_API_URL+video_id+'.json')
        data = response.json()[0]
        image_link = data['thumbnail_large']
        image_link = image_link.replace('wepb', 'jpg')
    except Exception:
        logging.exception (" ----------------  error while fetching video %s" % (video_link))
        image_link = DEFAULT_VIDEO_THUMB_URL    
    return image_link

def get_video_src(video_link):
    """ get video src link for iframe embed. 
        FIXME : Supports only vimeo so far """
    src_link = video_link
    if not('player.vimeo.com/video' in video_link):
        vid = video_link.rsplit('/', 1)[1]
        src_link = 'https://player.vimeo.com/video/'+vid
    return src_link

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
    return filename

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
    
def processModule(args,repoDir,outDir, module):
    """ fetch markdown files from [repoDir]/[module]/ folder. 
        [repoDir] has to be given as absolute path. [module] is just the name of the module
        If no outDir given, build files directly in same folder, else in [repoDir]/[outDir]/[module]/
    """
    # Folders
    moduleDir = os.path.join(repoDir, module)
    if not outDir:
        moduleOutDir = moduleDir
    else:
        moduleOutDir = os.path.join(repoDir,outDir,module)
    createDirs(moduleOutDir)

    # Fetch md file 
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

    # Parse md file
    with open(filein, encoding='utf-8') as md_file:
        m = model.Module(md_file, module)

    # write html,  XML, and JSon  files
    m.toHTMLFiles(moduleOutDir, args.feedback)
    m.toXMLMoodle(moduleOutDir)
    write_file(m.toGift(), moduleOutDir, '', module+'.questions_bank.gift.txt')
    write_file(m.toVideoList(), moduleOutDir, '', module+'.video_iframe_list.txt')
    mod_config = write_file(m.toJson(), moduleOutDir, '',  module+'.config.json')
    
    # We return module object and link to json-serialized file
    return m, mod_config