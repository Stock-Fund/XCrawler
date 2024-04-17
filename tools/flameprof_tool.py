import os
import webbrowser

source = "../pipeline.svg"
chrome_path = 'open -a /Applications/Google\\ Chrome.app %s'

def show_svg():
    assert os.path.exists(source)
    webbrowser.get(chrome_path).open(source)

show_svg()