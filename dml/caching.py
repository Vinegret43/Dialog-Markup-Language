
import os


cachedir = os.path.join(os.path.dirname(__file__), '.cache/')


def write_file(path, text):
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)
    path = os.path.abspath(path)
    dot_path = path.replace('/', '.')
    # Checking if an older version of this file exists in cache,
    # deleting it if it exists. It's necessary because otherwise
    # cache folder will grow pretty fast
    files = os.listdir(cachedir)
    files_without_mtimes = list(map(lambda x: x.split('-', 1)[1], files))
    if dot_path in files_without_mtimes:
        full_filename = files[files_without_mtimes.index(dot_path)]
        os.remove(os.path.join(cachedir, full_filename))
    # Creating a new cache file
    mtime = os.path.getmtime(path)
    cachefile = '{}-{}'.format(mtime, dot_path)
    with open(os.path.join(cachedir, cachefile), 'wb') as file:
        file.write(text)


def get_file(path):
    if not os.path.exists(cachedir):
        return None
    path = os.path.abspath(path)
    mtime = os.path.getmtime(path)
    # Checking if this cache file exists
    cachefile = '{}-{}'.format(mtime, path.replace('/', '.'))
    if cachefile not in os.listdir(cachedir):
        return None
    # If file exists, returning text from it
    with open(os.path.join(cachedir, cachefile), 'rb') as file:
        text = file.read()
    return text
