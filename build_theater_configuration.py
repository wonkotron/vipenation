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
    include_dirs = None
    def __init__(self, config_data):
        self._data = config_data.get("include_dirs", None)
        
        if self._data is None:
            print("[INFO] include_dirs field is empty in the configuration json")
            return
        else:
            include_dirs = []
            for path, include_data in self._data.items():
                include_dirs.append(IncludeDirsEntry(path, include_data))
            

class IncludeDirsEntry:
    _data = None
    
    path = None
    exclude_subdirs = None
    def __init__(self, path, include_data):
        self._data = include_data
        
        self.path = path
        self.exclude_subdirs = self._data.get("exclude_subdirs", [])
