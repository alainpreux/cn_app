#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
import logging
import shutil
import glob
import tarfile

from lxml import etree
from lxml import html
import markdown
from lxml.html.clean import Cleaner
from io import open
from jinja2 import Template, Environment, FileSystemLoader

import utils
import model

MARKDOWN_EXT = ['markdown.extensions.extra', 'superscript']
BASE_PATH = os.path.abspath(os.getcwd())
EDX_TEMPLATES_PATH = os.path.join(BASE_PATH, 'templates', 'toEDX' )
EDX_ADVANCED_MODULE_LIST = ['cnvideo', 'library_content']
EDX_GRADER_MAP = {
    'Activite':'Activite',
    'ActiviteAvancee':'Activite Avancee',
    'Comprehension':'Comprehension',
    'webcontent': None,
}

def generateEDXArchive(module, moduleOutDir):
    """ Given a module object and destination dir, generate EDX archive """

    jenv = Environment(loader=FileSystemLoader(EDX_TEMPLATES_PATH))
    jenv.filters['slugify'] = utils.cnslugify
    course_template = jenv.get_template("course.tmpl.xml")

    # Module data
    module.advanced_EDX_module_list = EDX_ADVANCED_MODULE_LIST.__str__()

    # Load grading policy template
    gpjson = os.path.join(EDX_TEMPLATES_PATH, 'policies', 'course', 'grading_policy.json')
    with open(gpjson, encoding='utf-8') as data_file:
        grading_policy = json.load(data_file)

    course_xml = course_template.render(module=module, grademap=EDX_GRADER_MAP)
    # create EDX archive temp folder
    edx_outdir = os.path.join(moduleOutDir, 'EDX')
    os.makedirs(edx_outdir)
    # generate files: html/webcontent | problem/(Activite|ActiviteAvancee|Comprehension)
    for sec in module.sections:
        for sub in sec.subsections:
            if sub.folder == 'webcontent': # these go to EDX/html/
                utils.write_file(sub.html_src, edx_outdir, 'html', sub.filename )
            elif sub.folder in ('Activite', 'ActiviteAvancee', 'Comprehension'):
                pass
    utils.write_file(course_xml, os.getcwd(), edx_outdir, 'course.xml')
