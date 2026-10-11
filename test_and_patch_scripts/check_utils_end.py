utils_path = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\utils-D8jN6fhl.js'
with open(utils_path, 'r', encoding='utf-8') as f:
    text = f.read()

end_chunk = text[-1500:]
print(end_chunk)
