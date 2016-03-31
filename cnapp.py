import os
import subprocess

from flask import Flask, send_from_directory
from werkzeug.routing import BaseConverter

# Configurations
app = Flask(__name__, static_url_path='', static_folder='build')
BASE_PATH = os.path.abspath(os.getcwd()) # we assume cnapp is run from base application folder
REPOS_DIR = 'repositories' # or give absolute path to repos dir
    
def init_repos():
    """ # open json file
        # check local clone exists 
        # if not create them """
    pass
            
    
@app.route('/build/<string:repo_user>/<string:repo_name>')
def build_repo(repo_user, repo_name):
    """ build repository """
    # TODO: 
    # - make it POST method
    # - check provenance of call ?
    # - retrieve branch 
    # - create subdir for other than master branch
    
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
    build_cmd = ("python src/toHTML.py -r %s" % repo_path)
    subprocess.check_output(build_cmd.split())

    return 'Build done !'
    
# Repo creation route methods    
@app.route('/new/<string:repo>')
def create_repo(repo):
    """ create new repo """
    # TODO:
    #   - make it POST
    #   - login user
    #   - create specific folder with exclusive rights for each user (safety)
    #   - create model for this : repo, user, platform, branch, other git username allowed to build, etc
    return 'Coming soon ;)'    
    
# Serving static pages >> FIXME: is it usefull ??
class WildcardConverter(BaseConverter):
    """ Converter to catch e.g 'site' and 'site/' """ 
    regex = r'(|/.*)'
    weight = 200
app.url_map.converters['wildcard'] = WildcardConverter

@app.route('/site/<string:repo_user>/<string:repo><wildcard:path>')
@app.route('/site/<string:repo_user>/<string:repo>/<path:path>')
def serve_static_site(repo_user, repo, path):
    print ("site path : =%s=" % path)
    if path == '/':
        path = 'index.html'
    elif path == "":
        pass # fixme: redirect browser to site/
    print ("site path AFTER: =%s=" % path)
    build_path = os.path.join(BASE_PATH, REPOS_DIR, repo_user, repo, 'build/last')
    return send_from_directory(build_path, path)

# Main 
if __name__ == '__main__':
    app.debug = True
    init_repos()
    app.run(host='0.0.0.0')