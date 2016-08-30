# -*- coding: utf-8 -*-

from __future__ import division
from datetime import datetime, timedelta
from io import open
import os
import shutil

import model
import logging


FOLDERS = ['Comprehension', 'Activite', 'ActiviteAvancee', 'webcontent']
STATIC_FOLDERS = ['static/js', 'static/img', 'static/svg', 'static/css', 'static/fonts']
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


def copyMediaDir(repoDir, moduleOutDir, module):
    """ Copy the media subdir if necessary to the dest """
    mediaDir = os.path.join(repoDir, module, "media")
    if os.path.isdir(mediaDir):
        try :
            shutil.copytree(mediaDir, os.path.join(moduleOutDir,'media'))
        except OSError as exception:
            logging.warn("%s already exists. Going to delete it",mediaDir)
            shutil.rmtree(os.path.join(moduleOutDir,'media'))
            shutil.copytree(mediaDir, os.path.join(moduleOutDir,'media'))


def prepareDestination(outDir):
    """ Create outDir and copy mandatory files""" 
    # first erase exising dir
    if os.path.exists(outDir):
        shutil.rmtree(outDir)
    if not os.path.isdir(outDir):
       if not os.path.exists(outDir):
           os.makedirs(outDir)
       else:
           print ("Cannot create %s " % (outDir))
           sys.exit(0)
    for d in STATIC_FOLDERS:
        dest = os.path.join(outDir, d)
        try :
            shutil.copytree(d, dest)
        except OSError as e:
            logging.warn("%s already exists, going to overwrite it",d)
            shutil.rmtree(dest)
            shutil.copytree(d, dest)

    
def fetchMarkdownFile(moduleDir):
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
    
    return filein
    
    