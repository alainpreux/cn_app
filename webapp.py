from io import open
import json
import logging
import os
import subprocess

from flask import Flask, send_from_directory, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.routing import BaseConverter

# Configurations
BASE_PATH = os.path.abspath(os.getcwd())
REPOS_DIR = 'repositories' # or give absolute path to repos dir
REPOS_FILE = 'repos.config.json'

# Create app
app = Flask(__name__, static_folder="repositories")
app.config.from_object(__name__)


def create_repo(repo_user, repo_name, repo_url):
    """ Create a dir repo_user/repo_name with clone of repo_url """
    repo_path = os.path.join(BASE_PATH, REPOS_DIR, repo_user, repo_name)
    current_path = os.path.abspath(os.getcwd())
    try:
        os.makedirs(repo_path)
        os.chdir(repo_path)
        git_cmd = ("git clone %s ." % repo_url)
        subprocess.check_output(git_cmd.split())
        
    except Exception as e:
        logging.warn("[creating repo] problem when creating %s/%s with url %s \n Error : %s " % (repo_user, repo_name, repo_url, e))
        pass 
    # In any case, go back to current_path
    os.chdir(current_path)
    logging.warn("[creating repo] successful creation of %s/%s with url %s" % (repo_user, repo_name, repo_url))
    return True

def init_repos(repos_file=REPOS_FILE):
    """ Admin command that initialize registered repositories:
        - open json file
        - check local clone exists 
        - if not create them """
    logging.warn(" initialize repos %s" % repos_file)
    with open(repos_file, encoding='utf-8') as repos_data_file:
        repos_data = json.load(repos_data_file)
    
    current_path = os.path.abspath(os.getcwd())
    for repo in repos_data['repositories']:
        # check path repos_dir/repo_user/repo_name exists
        try:
            os.chdir(os.path.join(BASE_PATH, REPOS_DIR, repo['repo_user'], repo['repo_name']))
            # if so, updtate it
            git_cmd = "git pull origin master"
            subprocess.check_output(git_cmd.split())
        except OSError as err:
            logging.warn(" repo is in data but does not (yet) exist : %s" % err)        
            # if not, create and initialize it with repo_url
            logging.warn(" creating : %s/%s" % (repo['repo_user'], repo['repo_name']))        
            create_repo(repo['repo_user'], repo['repo_name'], repo['repo_url'])
        os.chdir(current_path)
    
    print(" Initialization done. Now running app")
    return True
    
@app.route('/')            
@app.route('/repos/')
def list_repos():
    """ Home page that list available repos """
    return ' Liste des repos '

@app.route('/repos/<string:repo_user>/<string:repo_name>')
def detail_repo(repo_user, repo_name):
    """ give detail for selected repo """
    return render_template('repo.html')
    
@app.route('/build/<repo_user>/<repo_name>', methods=['GET', 'POST'])
def build_repo(repo_user, repo_name):
    """ build repository  """
    # TODO: retrieve branch and create subdir for other than master branch
    # 1. cd to repo path
    repo_path = os.path.join(BASE_PATH, REPOS_DIR, repo_user, repo_name)
    try:
        os.chdir(repo_path)
    except Exception as e:
        return ('ERROR : Repository not settup properly or non existing repository submitted')
    # 2. git pull origin [branch:'master']
    git_cmd = "git pull origin master"
    subprocess.check_output(git_cmd.split())
    # 3. build with BASE_PATH/src/toHTML.py 
    os.chdir(BASE_PATH)
    build_cmd = ("python src/cnExport.py -r %s -i" % repo_path)
    subprocess.check_output(build_cmd.split())

    return redirect(url_for('serve_static_site', repo_user=repo_user, repo=repo_name, path=''))
    
# Repo creation route methods    
@app.route('/new/<repo>')
def new_repo(repo):
    """ create new repo """
    # TODO:
    #   - make it POST
    #   - create specific folder with exclusive rights for each user (safety)
    #   - create model for this : repo, user, platform, branch, other git username allowed to build, etc
    return 'Coming soon ;)'    
    
# Serving static pages
class WildcardConverter(BaseConverter):
    """ Converter to catch e.g 'site' and 'site/' """ 
    regex = r'(|/.*)'
    weight = 200
app.url_map.converters['wildcard'] = WildcardConverter

@app.route('/site/<repo_user>/<repo><wildcard:path>')
@app.route('/site/<repo_user>/<repo>/<path:path>')
def serve_static_site(repo_user, repo, path):
    logging.warn("site path : =%s=" % path)
    if path == '/':
        path = 'index.html'
    elif path == "":
        pass # fixme: redirect browser to site/
    logging.warn("site path AFTER: =%s=" % path)
    build_path = os.path.join(BASE_PATH, REPOS_DIR, repo_user, repo, 'build/last')
    return send_from_directory(build_path, path)

@app.after_request
def add_header(response):
    """ Add headers to disable cache """
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

# Main 
if __name__ == '__main__':
    
    logging.basicConfig(filename='logs/cnapp.log',filemode='w',level='WARNING')
    init_repos()
    app.debug = True
    app.run(use_reloader=False)