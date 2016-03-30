import os
import subprocess

from flask import Flask, send_from_directory
from werkzeug.routing import BaseConverter

app = Flask(__name__, static_url_path='', static_folder='build')
    
@app.route('/new/<string:repo>')
def create_repo(repo):
    """ create new repo """
    # TODO:
    #   - make it POST
    #   - login user
    #   - create specific folder with exclusive rights for each user (safety)
    #   - create model for this : repo, user, platform, branch, other git username allowed to build, etc
    return 'Coming soon ;)'    
    
@app.route('/build/<string:repo>')
def build_repo(repo):
    """
        build repository
    """
    # TODO:
    #   - make it POST
    
    # 1. cd to BASE_PATH/repo
    app_abs_path = os.path.abspath(os.getcwd())
    base_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    repo_path = os.path.join(base_path, repo)
    try:
        os.chdir(repo_path)
    except Exception as e:
        return ('ERROR : Repository not settup properly or non existing repository submitted')
    # 2. git pull origin [branch:'master']
    git_cmd = "git pull origin master"
    subprocess.check_output(git_cmd.split())
    # 3. build with base_path/src/toHTML.py 
    os.chdir(app_abs_path)
    build_cmd = ("python src/toHTML.py -r %s" % repo)
    subprocess.check_output(build_cmd.split())

    return 'Build done !'

# Serving static pages

class WildcardConverter(BaseConverter):
    """ Converter to catch e.g 'site' and 'site/' """ 
    regex = r'(|/.*)'
    weight = 200
app.url_map.converters['wildcard'] = WildcardConverter

@app.route('/site<wildcard:path>')
@app.route('/site/<path:path>')
def serve_static_site(path):
    print ("site path : =%s=" % path)
    if path == '/':
        path = 'index.html'
    elif path == "":
        pass # fixme: redirect browser to site/
    print ("site path AFTER: =%s=" % path)
    return send_from_directory('build/last', path)

if __name__ == '__main__':
    app.debug = True
    app.run()