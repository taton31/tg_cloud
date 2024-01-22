class Progress():
    progress_dict = dict()
    def set_progress(self, key, msg_id, val):
        if key not in self.progress_dict: self.progress_dict[key] = dict()
        self.progress_dict[key][msg_id] = val

    def get_progress(self, key):
        return round(sum(self.progress_dict.get(key, {'a': 0}).values()))  