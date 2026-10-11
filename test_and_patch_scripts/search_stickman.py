import os

def search_text(base_dirs, term):
    for base in base_dirs:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith(('.js', '.html', '.json', '.css')):
                    p = os.path.join(root, file)
                    try:
                        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                            c = f.read()
                            if term.lower() in c.lower():
                                print(f"Found '{term}' in {p}")
                    except Exception as e:
                        pass

search_text(['E:/stickman-video-automation/extensions', 'C:/Users/Ali/Desktop/meta automation'], 'STICKMAN STUDIO')
