#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys
import logging
import shutil
import glob

from lxml import etree
from lxml import html
import markdown
from yattag import indent
from yattag import Doc
from lxml.html.clean import Cleaner
from io import open
from jinja2 import Template, Environment, FileSystemLoader

import utils
import toIMS
import model

MARKDOWN_EXT = ['markdown.extensions.extra', 'superscript']
BASE_PATH = os.path.abspath(os.getcwd())
TEMPLATES_PATH = os.path.join(BASE_PATH, 'templates' )


def write_iframe_code(video_link):
    return '<div class="iframe_cont"><iframe allowfullscreen="" mozallowfullscreen="" webkitallowfullscreen="" data-src="'+video_link+'"></iframe></div>'
    

def parse_content(href, module, outModuleDir, rewrite_iframe_src=True):
    """ open file and replace media links and src for iframes """
    try:
        with open(href, 'r', encoding='utf-8') as file:
            htmltext = file.read()
    except Exception as e:
        logging.exception("Exception reading %s: %s " % (href,e))
        return ''

    if not htmltext:
        return ''
    
    tree = html.fromstring(htmltext)
    # Rewrite image links: for each module file, media dir is one step above (../media/)
    # with html export, medias are accessed from index.html in root dir, so we have 
    # to reconstruct the whole path
    try:
        for element, attribute, link, pos in tree.iterlinks():
            newlink = link.replace("../media", module+"/media")
            element.set(attribute, newlink)
    except Exception as e:
        logging.exception("Exception rewriting/removing links %s" % e)

    return html.tostring(tree, encoding='utf-8').decode('utf-8')

def generateMenuSubsections(idSection, subsections,doc,tag,text):
    # looping through subsections, skipping non html files
    for idSubSection, subsection in enumerate(subsections):
        # 1st subsection active by default
        if idSubSection == 0:
            active_sub = " active"
        else:
            active_sub = ""
        subsection_id = "subsec_"+str(idSection)+'_'+str(idSubSection)
        if subsection['folder'] != 'correction':
            with tag('a', href="#", data_sec_id=subsection_id, klass="subsection "+subsection['folder']+active_sub):
                text(str(idSection+1)+'.'+str(idSubSection+1)+' '+
                     subsection['title'])


def generateMenuSections(data,doc,tag,text): 
    for idSection, section in enumerate(data["sections"]):
        # 1st section active by default
        if idSection == 0:
            active_sec = " active"
            display = " display:block"
        else:
            active_sec = ""
            display = ""
        section_id = "sec_"+str(idSection)
        with tag('li'):
            with tag('a', href="#", data_sec_id=section_id, klass="section"+active_sec):
                text(section['num']+' '+section['title'])
            with tag('p', style=display):
                generateMenuSubsections(idSection,section['subsections'],doc,tag,text)
    # add link to download section
    with tag('li', style="border-top: 2px solid lightgray;"):
        with tag('a', href="#", data_sec_id="sec_A", klass="section"):
            text("Annexe: Réutiliser ce module")
            
            
def generateVideo(doc,tag,text,videos,display,subsection,subsec_text):
    for idVid, video in enumerate(videos):
        # add text only 1st time
        if idVid == 0:
            # add text in fancybox lightbox
            text_id = subsection['num']+"_"+str(idVid)
            with tag('div', klass="inline fancybox", href="#"+text_id):
                text('Version Texte du cours')
                with tag('div', klass="mini-text"):
                    doc.asis(subsec_text)
            with tag('div', style="display:none"):
                with tag('div', id=text_id, klass="fancy-text"):
                    doc.asis(subsec_text)
        # go new line for each video after 1st video
        if idVid > 0:
            doc.asis('<br />')
        # add iframe code
        iframe_code = write_iframe_code(video['video_link'])
        if display=="true": # for very first subsection, keep normal iframe src 
            iframe_code = iframe_code.replace('data-src', 'src')
        doc.asis(iframe_code)
        doc.asis("\n\n")
        
def generateDownloadSection(data, doc,tag,text,module, outModuleDir):
    ims_path = module+'/'+data["ims_archive_path"]
    with tag('section', id="sec_A", style="display:none"):
        with tag('p', klass="fil_ariane"):
            text("Annexe A: Réutiliser ce module")
        with tag('p'):
            text("Voici les liens vers les fichiers téléchargeables vous permettant de réutiliser ce module de cours:")
        with tag('ul'):
            if len(data["ims_archive_path"]) > 0:
                with tag('li'):
                    text("Archive IMS CC utilisable dans les LMS Moodle, Claroline, Blackboard, etc: ")
                    with tag('a', href=ims_path):
                        text(data["ims_archive_path"])
            

def generateMainContent(data, doc,tag,text,module, outModuleDir):
    # Print main content
    doc.asis('<!--  MAIN CONTENT -->')
    with tag('main', klass="content"):
        # Loop through sections
        for idSection,section in enumerate(data["sections"]):
            
#            section_id = "sec_"+str(idSection)
#            href = os.path.join(module_folder, section['filename'])
#            with tag('section', id=section_id, style=("display:none")):
#                doc.asis(parse_content(href, module_folder))
            # Loop through subsections
            for idSubsection,subsection in enumerate(section['subsections']):
                if subsection['folder'] != 'correction':
                    # load 1st subsec by default, rest is hidden
                    if idSubsection==0 and idSection == 0:
                        display = "true"
                    else:
                        display = "none"
                    subsection_id = "subsec_"+str(idSection)+'_'+str(idSubsection)
                    with tag('section', id=subsection_id, style="display:"+display):
                        # fil d'arianne
                        with tag('p', klass='fil_ariane'):
                            text(section['title']+' | '+subsection['title'])
                        href = os.path.join(outModuleDir, subsection['folder'],subsection['filename'])
                        subsec_text = parse_content(href, module, outModuleDir)
                        if "videos" in subsection and len(subsection["videos"]) != 0 :
                            generateVideo(doc,tag,text,subsection["videos"],display,subsection,subsec_text)
                        else: # print subsection text asis                        
                            if href.endswith(".html"):
                                doc.asis(subsec_text)
        # add download section
        generateDownloadSection(data,doc,tag,text,module,outModuleDir)

def writeHtml(module, outModuleDir, html):
    module_file_name = os.path.join(outModuleDir, module)+'.html'
    moduleHtml = open(module_file_name, 'w', encoding='utf-8')
    moduleHtml.write(html)
    moduleHtml.close()
    
    
def generateModuleHtml(data, module, outModuleDir):
    """ parse data from config file 'moduleX.config.json' and generate a moduleX html file """
    # 
    # # create magic yattag triple
    # doc, tag, text = Doc().tagtext()
    # 
    # doc.asis('<!--  NAVIGATION MENU -->')
    # with tag('nav', klass="menu accordion"):
    #     with tag('h3'):
    #         text(data["title"])
    #     with tag('ul'):
    #         generateMenuSections(data,doc,tag,text)
    #         
    # generateMainContent(data,doc,tag,text,module, outModuleDir)
    jenv = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    module_template = jenv.get_template("module.html")
    html = module_template.render(module=data)
    writeHtml(module, outModuleDir, html)

def processModule(module,repoDir,outDir, feedback_option, ims_option):
    """ given input paramaters, process a module  """
    outModuleDir = os.path.join(repoDir,outDir,module)
    
    # generate config file: config file for each module is named [module_folder].config.json
    mod_obj, mod_config = utils.processModule(module,repoDir,outDir, feedback_option)
    
    # Copy the media subdir if necessary to the dest 
    mediaDir = os.path.join(repoDir, module, "media")
    if os.path.isdir(mediaDir):
        try :
            shutil.copytree(mediaDir, os.path.join(outModuleDir,'media'))
        except OSError as exception:
            logging.warn("%s already exists. Going to delete it",mediaDir)
            shutil.rmtree(os.path.join(outModuleDir,'media'))
            shutil.copytree(mediaDir, os.path.join(outModuleDir,'media'))
            
    # if chosen, generate IMS archive
    if ims_option:
        mod_obj.ims_archive_path = toIMS.generateImsArchive(module, outModuleDir)
        logging.warn('*Path to IMS = %s*' % mod_obj.ims_archive_path)
    # Generate module html file from JSON file
    # ** FIXME ** use Jinja2 template and directly module object!!
    with open(mod_config, encoding='utf-8') as mod_data_file:
        mod_data = json.load(mod_data_file)
        mod_data['ims_archive_path'] = mod_obj.ims_archive_path
    generateModuleHtml(mod_data, module, outModuleDir)
    
        
    return mod_obj

def processRepository(args, repoDir, outDir):
    """ takes arguments and directories and process repository  """
    os.chdir(repoDir)
    course_obj = model.CourseProgram(repoDir)
    # first checks
    if args.modules == None:
        listt = glob.glob("module[0-9]")
        args.modules = sorted(listt,key=lambda a: a.lstrip('module'))
        
    for module in args.modules:
        logging.info("\nStart Processing %s",module)
        course_obj.modules.append(processModule(module, repoDir, outDir, args.feedback, args.ims))
    
    return course_obj
     

def buildSite(course_obj, repoDir, outDir):
    """ Generate full site from result of parsing repository """    
    
    jenv = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    site_template = jenv.get_template("site_layout.html")
    #if found, copy logo.png, else use default
    logo_files = glob.glob(os.path.join(repoDir, 'logo.*'))
    if len(logo_files) > 0:
        logo = logo_files[0]
    else:# use default one
        logo = os.path.join(TEMPLATES_PATH, 'logo.png') 
    try:
        shutil.copy(logo, outDir)
    except Exception as e:
        logging.warn(" Error while copying logo file %s" % e)
        pass
    
    ## open and parse 1st line title.md
    try:
        title_file = os.path.join(repoDir, 'title.md')
        with open(title_file, 'r', encoding='utf-8') as f:
            course_obj.title = f.read().strip()
    except Exception as e:
        logging.warn(" Error while parsing title file %s" % e)
        pass
    
    # Create site index.html with home.md content    
    ## open and parse home.md
    try:
        home_file = os.path.join(repoDir, 'home.md')
        with open(home_file, 'r', encoding='utf-8') as f:
            home_data = f.read()
        home_html = markdown.markdown(home_data, MARKDOWN_EXT)
    except Exception as err:
        ## use default from template
        logging.error(" Cannot parse home markdown ")
        with open(os.path.join(TEMPLATES_PATH, 'default_home.html'), 'r', encoding='utf-8') as f:
            home_html = f.read()
    ## write index.html file
    html = site_template.render(course=course_obj, module_content=home_html,body_class="home")
    utils.write_file(html, os.getcwd(), outDir, 'index.html')
    
    # Loop through modules
    for module in course_obj.modules:
        in_module_file = os.path.join(outDir, module.module, module.module+".html")
        with open(in_module_file, 'r', encoding='utf-8') as f:
            data=f.read()
        html = site_template.render(course=course_obj, module_content=data, body_class="modules")
        utils.write_file(html, os.getcwd(), outDir, module.module+'.html')



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
    for d in ['static/js', 'static/img', 'static/svg', 'static/css', 'static/fonts']:
        dest = os.path.join(outDir, d)
        try :
            shutil.copytree(d, dest)
        except OSError as e:
            logging.warn("%s already exists, going to overwrite it",d)
            shutil.rmtree(dest)
            shutil.copytree(d, dest)
    
            
############### main ################
if __name__ == "__main__":

    # utf8 hack, python 2 only !!
    if sys.version_info[0] == 2:
        print ("reload default encoding")
        reload(sys)
        sys.setdefaultencoding('utf8')
    
    import argparse
    parser = argparse.ArgumentParser(description="Parses markdown files and generates a website using index.tmpl in the current directory. Default is to process and all folders 'module*'.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--modules",help="module folders",nargs='*')
    parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level", default='WARNING')
    parser.add_argument("-r", "--repository", help="Set the repositorie source dir containing the moduleX dirs, given as absolute or relative to cn_app dir", default='repositories/culturenumerique/cn_modules')
    parser.add_argument("-d", "--destination", help="Set the destination dir", default='build')
    parser.add_argument("-f", "--feedback", action='store_true', help="Set the destination dir", default=False)
    parser.add_argument("-i", "--ims", action='store_true', help="Also generate IMS archive for each module", default=False)
    args = parser.parse_args()
    
    # set logging file and level from args
    logging.basicConfig(filename='logs/toHTML.log',filemode='w',level=getattr(logging, args.logLevel))

    # Setting up paths and directories
    ## repo path
    if os.path.isabs(args.repository):
        repoDir = args.repository
    else:    
        repoDir = os.path.join(BASE_PATH, args.repository)
    logging.warn("repository directory path : %s" % repoDir)
    ## Check repo exists, otherwise exit
    if not(os.path.exists(repoDir)):
        sys.exit("Error : repository directory provided does not exist")
    ## check destination path and build outDir
    if (args.destination == '.') or (args.destination.rstrip('/') == os.getcwd()):
        sys.exit("Error: cannot build within current directory.")
    if os.path.isabs(args.destination):
        outDir = args.destination
    else: 
        outDir = os.path.join(repoDir, args.destination)
    ## check destination
    prepareDestination(outDir)
    
    # Process repository
    course_obj = processRepository(args, repoDir, outDir)
    
    # Build site
    
    buildSite(course_obj, repoDir, outDir)        
        
    # Exit and print path to build files:
    os.chdir(BASE_PATH)
    print("**Build successful!** See result in : %s" % outDir)
    sys.exit(0)