import os

def check():
    base = 'e:/stickman-video-automation'
    for root, dirs, files in os.walk(base):
        if 'manifest.json' in files:
            print('Extension manifest found at:', root)
        # don't traverse too deep in node_modules or .git
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist', 'projects_media']]

if __name__ == '__main__':
    check()
