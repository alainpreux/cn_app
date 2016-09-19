#!/usr/bin/python
# -*- coding: utf-8 -*-
#
######################################################################################
#
#    Data model for Courses and Activities. The module provides
#    parse tools for markdown files following the
#    Culture Numérique guidelines. Outputs
#       - JSON config file
#       - HTML files (a cut out of the file in html and gift files, orderered in a folder structure)
#       - HTML views
#       - IMSCC archive (Open EDX coming soon)
#
######################################################################################


import sys
import re
import json
import markdown
import requests
import logging
from unidecode import unidecode
from inspect import isclass

from lxml import etree
from lxml import html
from slugify import slugify

from fromGIFT import extract_questions, process_questions
from toIMS import create_ims_test, create_empty_ims_test
import utils


MARKDOWN_EXT = ['markdown.extensions.extra', 'superscript']
VIDEO_THUMB_API_URL = 'https://vimeo.com/api/v2/video/'
DEFAULT_VIDEO_THUMB_URL = 'https://i.vimeocdn.com/video/536038298_640.jpg'
DEFAULT_BASE_URL = 'http://culturenumerique.univ-lille3.fr'

# Regexps
reEndHead = re.compile('^#')
reStartSection = re.compile('^#\s+(?P<title>.*)$')
reStartSubsection = re.compile('^##\s+(?P<title>.*)$')
reStartActivity = re.compile('^```(?P<type>.*)$')
reEndActivity = re.compile('^```\s*$')
reMetaData = re.compile('^(?P<meta>.*?):\s*(?P<value>.*)\s*$')

def goodActivity(match):
    m = sys.modules[__name__]
    typeSection = re.sub('[ ._-]','',unidecode(match.group('type')).title())
    if typeSection in m.__dict__ :
        act = getattr(m,typeSection)
        if isclass(act):
            return act
    return None


class ComplexEncoder(json.JSONEncoder):
    ''' Encoder for Json serialization: just delete recursive structures'''
    def default(self, obj):
        if isinstance(obj, Section) or isinstance(obj,Module):
            return obj.__dict__
        elif isinstance(obj, Subsection):
            d = obj.__dict__.copy()
            del d['section']
            if isinstance(obj,AnyActivity):
                del d['questions']
            return d
        return json.JSONEncoder.default(self, obj)



class Subsection:
    """
    Abstract class for any type of subsection: lectures and activities
    - folders property equals the type (name of the class)
    - num subsection number based on the section number
    """
    num = 1
    def __init__(self, section):
        self.section = section
        self.num = self.section.num+'-'+str(Subsection.num)
        self.videos = []
        Subsection.num +=1

    def getFilename(self):
        self.filename = slugify(self.num+self.title)+'_'+self.folder+'.html'
        return self.filename

    def toHTMLFile(self,outDir, feedback_option):
        utils.write_file(self.toHTML(feedback_option), outDir, self.folder, self.getFilename())

    def toGift(self):
        return ''

    def toXMLMoodle(self, outDir):
        pass

    def absolutizeMediaLinks(self):
        self.src = re.sub('\]\(\s*(\.\/)*\s*media/', ']('+self.section.base_url+'/'+self.section.module+'/media/', self.src)

class Cours(Subsection):
    """ Class for a lecture"""
    def __init__(self, section, file=None, src='' ,title = 'Cours'):
        Subsection.__init__(self,section)
        self.title = title
        self.folder = 'webcontent'
        self.videos = []
        if src:
            self.src= src
        else:
            self.src=''
            self.parse(file)
        self.absolutizeMediaLinks()


    def parse(self,f):
        ''' Read lines in f until the end of the course '''
        self.lastLine = f.readline()
        while self.lastLine and not reStartSection.match(self.lastLine) and not reStartSubsection.match(self.lastLine) :
            # Is it really the end of the section?
            # blocks that are not activities are included!
            match = reStartActivity.match(self.lastLine)
            if match and goodActivity(match):
                return
            self.src += self.lastLine
            self.lastLine = f.readline()


    def toHTML(self, feedback_option=False):
        self.html_src = markdown.markdown(self.src, MARKDOWN_EXT)
        # detect cours_video video links
        self.videos = self.detectVideoLinks()
        if (len(self.videos) > 0):
            logging.info("detected cours_video links")
        # detect cours_video video links
        self.lienvideos = self.detectVideoLinks(class_='lien_video')
        if (len(self.videos) > 0):
            logging.info("detected lien_video links")
        self.html_src = utils.iframize_video_anchors(self.html_src, 'lien_video')
        self.html_src = utils.add_target_blank(self.html_src)
        return self.html_src


    def detectVideoLinks(self, class_='cours_video'):
        videos_findall = re.findall('^\[(?P<video_title>.*)\]\s*\((?P<video_link>.*)\){:\s*\.'+class_+'\s*.*}', self.src, flags=re.M)
        videos_list = []
        for video_match in videos_findall:
            new_video = {
                'video_title':video_match[0],
                'video_link':video_match[1].strip(),
                'video_src_link':utils.get_video_src(video_match[1].strip()),
                'video_thumbnail':DEFAULT_VIDEO_THUMB_URL
            }
            videos_list.append(new_video)
        return videos_list

    def videoIframeList(self):
        video_list = "\n"+self.num+' '+self.title+'\n\n'
        video_list += "** Videos de cours : **\n\n"
        for v in self.videos:
            video_list += ''
            video_list += '<iframe src='+v['video_src_link']+' width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>\n'
        if len(self.lienvideos) > 0:
            video_list += "\n** Videos de contenu : **\n\n"
        for v in self.lienvideos:
            video_list += '    - titre : %s \n' % v['video_title']
        return video_list

class AnyActivity(Subsection):
    """ Abstract class for any activity """
    def __init__(self,section,f):
        Subsection.__init__(self,section)
        self.src = ''
        self.parse(f)
        self.absolutizeMediaLinks()
        self.questions = process_questions(extract_questions(self.src))


    def parse(self,f):
        ''' Read lines in f until the end of the activity '''
        self.lastLine = f.readline()
        while self.lastLine and not reEndActivity.match(self.lastLine):
            self.src += self.lastLine
            self.lastLine = f.readline()

    def toGift(self):
        gift_src=''
        for question in self.questions:
            gift_src+='\n'+question.gift_src+'\n'
        return gift_src

    def toHTML(self, feedback_option=False):
        self.html_src = ''
        for question in self.questions:
            # append each question to html output
            self.html_src+=question.to_html(feedback_option)
            if self.html_src == '': # fallback when question is not yet properly formated
                self.html_src = '<p>'+self.src+'</p>'
            # post-process Gift source replacing markdown formated questions text by html equivalent
            if question.text_format in (("markdown")):
                question.md_src_to_html()
        # add "target="_blank" to all anchors
        try:
            tree = html.fromstring(self.html_src)
            for link in tree.xpath('//a'):
                link.attrib['target']="_blank"
            self.html_src = html.tostring(tree, encoding='utf-8').decode('utf-8')
        except:
            logging.exception("=== Error finding anchors in html src: %s" % self.html_src)

        return self.html_src

    def toXMLMoodle(self,outDir):
        # a) depending on the type, get max number of attempts for the test
        if isinstance(self, Comprehension):
            max_attempts = '1'
        else:
            max_attempts = 'unlimited'
        # b) write empty xml test file for moodle export FIXME: moodle specific, do it only when asked
        #xml_src = create_empty_ims_test(self.num+'_'+slugify(self.title), self.num, self.title, max_attempts)
        xml_src = create_ims_test(self.questions, self.num+'_'+slugify(self.title), self.title)
        filename = self.getFilename()
        xml_filename = filename.replace('html', 'xml')
        #   write xml file at same location
        utils.write_file(xml_src, outDir, self.folder , xml_filename)

class Comprehension(AnyActivity):

    def __init__(self, section, src):
        AnyActivity.__init__(self,section,src)
        self.title = 'Compréhension'
        self.folder = 'Comprehension'

class Activite(AnyActivity):

    def __init__(self, section, src):
        AnyActivity.__init__(self,section,src)
        self.title = 'Activité'
        self.folder = 'Activite'

class ActiviteAvancee(AnyActivity):

    def __init__(self, section, src):
        AnyActivity.__init__(self,section,src)
        self.title = 'Activité avancée'
        self.folder = 'ActiviteAvancee'


class Section:
    num = 1

    def __init__(self,title,f,module, base_url=DEFAULT_BASE_URL):
        self.title = title
        self.subsections = []
        self.num = str(Section.num)
        self.module = module
        self.base_url = base_url
        self.parse(f)
        Section.num +=1
        Subsection.num=1

    def parse(self, f):
        body = ''
        self.lastLine = f.readline()
        while self.lastLine:
            # is it a new section ?
            match = reStartSection.match(self.lastLine)
            if match:
                # for sections with only text:
                if body and not body.isspace():
                    self.subsections.append(Cours(self,src=body))
                break
            else:
                # is it a new subsection ?
                match = reStartSubsection.match(self.lastLine)
                if match :
                    # should I create a subsection (text just below a section
                    # or between activities
                    if body and not body.isspace():
                        self.subsections.append(Cours(self,src=body))
                    sub = Cours(self,file=f,title=match.group('title'))
                    self.subsections.append(sub)
                    # The next line is the last line read in the parse of the subsection
                    self.lastLine = sub.lastLine
                    body = ''
                else:
                    # is it an activity
                    match = reStartActivity.match(self.lastLine)
                    if match :
                        act = goodActivity(match)
                        if act:
                            # should I create a subsection (text just below a section
                            # or between activities
                            if body and not body.isspace():
                                self.subsections.append(Cours(self,src=body))
                                body = ''
                            self.subsections.append(act(self,f))
                            # read a new line after the end of blocks
                            self.lastLine = f.readline()
                        else:
                            logging.warning ("Unknown activity type %s",self.lastLine)
                            body += self.lastLine
                            self.lastLine = f.readline()
                    else:
                        # no match, add the line to the body and read a new line
                        body += self.lastLine
                        self.lastLine = f.readline()


    def toHTMLFiles(self,outDir, feedback_option=False):
        for sub in self.subsections:
            sub.toHTMLFile(outDir, feedback_option)

    def toXMLMoodle(self, outDir):
        for sub in self.subsections:
            sub.toXMLMoodle(outDir)

    def toGift(self):
        allGifts = ""
        for sub in self.subsections:
            if isinstance(sub, AnyActivity):
                # Add category here
                allGifts += "\n$CATEGORY: $course$/Quiz Bank '"+sub.num+' '+sub.title+"'\n\n"
                allGifts += sub.toGift()
        return allGifts

    def toVideoList(self):
        video_list = ""
        for sub in self.subsections:
            if isinstance(sub, Cours):
                video_list += sub.videoIframeList()
        return video_list

class Module:
    """ Module structure"""

    def __init__(self,f, module, base_url=DEFAULT_BASE_URL):
        self.sections = []
        Section.num = 1
        self.module = module
        self.ims_archive_path = ''
        self.language = 'fr'
        self.title = 'Titre long'
        self.menutitle = 'Titre'
        self.author = 'culture numerique'
        self.css = 'http://culturenumerique.univ-lille3.fr/css/base.css'
        self.base_url = base_url
        self.parse(f)

    def parseHead(self,f) :
        """ Captures meta-data  """
        l = f.readline()
        while l and not reEndHead.match(l) :
            m = reMetaData.match(l)
            if m:
                setattr(self, m.group('meta').lower(), m.group('value'))
            l = f.readline()
        return l

    def toJson(self):
        return json.dumps(self, sort_keys=True,
                          indent=4, separators=(',', ': '),cls=ComplexEncoder)

    def parse(self,f):
        #  A. split sections
        ## up to first section
        l = self.parseHead(f)
        match = reStartSection.match(l)
        while l and match:
            s = Section(match.group('title'),f, self.module, self.base_url)
            self.sections.append( s )
            l = s.lastLine
            match = reStartSection.match(l)


    def toHTMLFiles(self, outDir, feedback_option=False):
        for s in self.sections:
            s.toHTMLFiles(outDir, feedback_option)

    def toXMLMoodle(self, outDir):
        for s in self.sections:
            s.toXMLMoodle(outDir)

    def toGift(self):
        """a text resource with all questions with a category / used for import into moodle"""
        questions_bank = ""
        for s in self.sections:
            questions_bank += s.toGift()

        # write questions bank file
        return questions_bank

    def toVideoList(self):
        """ a text resource with all video iframe codes """
        video_list = ""
        for s in self.sections:
            video_list += s.toVideoList()+'\n\n'

        return video_list


class CourseProgram:
    """ A course program is made of one or several course modules """

    def __init__(self, repository):
        """ A CP is initiated from a repository containing global paramaters file (logo.jpg, title.md, home.md)
         and folders moduleX containing module file and medias """
        self.modules = []
        self.repository = repository
        self.title = 'Culture Numérique'
        self.logo_path = 'logo.png'


############### main ################
if __name__ == "__main__":
    import io

    f = io.StringIO("""
LANGUAGE:   FR
TITLE:   Représentation numérique de l'information : Test Module
AUTHOR:     Culture numérique
CSS: http://culturenumerique.univ-lille3.fr/css/base.css

# sect 11111
contenu sd
## subsec AAAA
aaa
## subs BBBB
contenu b
# sect CCCC
cont cccc
## subsec DDDD
ddddd
# sect 222222
dfg
```
code
```
dfg
dfgxs

## sub EEEEE
```truc
sdsdf
```
# sect 333

avant activite

```activité
ceci est une acticité 1
```
```activité
ceci est une acticité 2
```
milieu activite
```activité-avancee
ceci est une acticité 3
```

apres activite
""")

    m = Module(f)

    print (m.toJson())

    module_folder = "tmp"
    utils.createDirs(module_folder)

    m.toHTMLFiles(module_folder)
    m.toXMLMoodle(module_folder)
