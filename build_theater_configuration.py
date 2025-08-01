import json

class Configuration:
    _data = None
    include_dirs = None

    def __init__(self, config_path):
        if config_path is None:
            config_path = "E:\\dev\\bms\\vipenation\\theaters\\build_ag_ito.json"
        with open(config_path, 'r') as f:
            self._data = json.load(f)
        
        self.include_dirs = IncludeDirs(self._data)


class IncludeDirs:
    _data = None
    entries = None
    def __init__(self, config_data):
        self._data = config_data.get("include_dirs", None)
        
        if self._data is None:
            print("[INFO] include_dirs field is empty in the configuration json")
            return
        else:
            self.entries = []
            for path, include_data in self._data.items():
                self.entries.append(IncludeDirsEntry(path, include_data))
            

class IncludeDirsEntry:
    _data = None
    
    path = None
    exclude = None  # to be used in shutil.ignore_patterns()

    def __init__(self, path, include_data):
        self._data = include_data
        
        self.path = path
        self.exclude = self._data.get("exclude", [])
