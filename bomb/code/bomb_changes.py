# Add code to this file
class phase_changes:
    def __init__(self, toggle_change):
        self._toggle_change = toggle_change

    def get_toggle_change(self):
        return self._toggle_change

    def set_toggle_change(self,toggle_change):
        self._toggle_change = toggle_change

    toggle_change = property(get_toggle_change, set_toggle_change)

