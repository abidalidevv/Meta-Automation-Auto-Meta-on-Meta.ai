pm_path = r'E:\stickman-video-automation\studio\server\profile_manager.js'

with open(pm_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the premature class closing bracket
premature = """    return {
      active_count: list.length,
      processes: list,
      chrome_path: this.chromePath,
      telemetry
    };
  }
}"""

fixed_premature = """    return {
      active_count: list.length,
      processes: list,
      chrome_path: this.chromePath,
      telemetry
    };
  }"""

if premature in content:
    content = content.replace(premature, fixed_premature)
    # Ensure there is a closing } before module.exports
    export_str = "module.exports = new BrowserProfileManager();"
    if not content.rstrip().endswith("}\n\n" + export_str) and not content.rstrip().endswith("}\n" + export_str):
        # find last occurrence of export_str
        idx = content.rfind(export_str)
        content = content[:idx] + "}\n\n" + export_str

    with open(pm_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully fixed class closing in profile_manager.js')
else:
    print('Premature closing not found directly')
