with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the Modal M2 payload to include character_image_base64
old_payload = """    character_name: char_name,
      character_description: char_desc
    };"""

new_payload = """    character_name: char_name,
      character_description: char_desc,
      character_image_base64: modalCharBase64_M2
    };"""

if old_payload in text:
    text = text.replace(old_payload, new_payload, 1)
    with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully added character_image_base64 to Modal M2 payload!")
else:
    # Search for it
    idx = text.find('character_description: char_desc')
    print("Context:")
    print(repr(text[idx-60:idx+80]))
