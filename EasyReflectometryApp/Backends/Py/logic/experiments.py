from easyreflectometry import Project as ProjectLib


class Experiments:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._current_index = 0

    def available(self) -> list[str]:
        experiments_name = []
        try:
            experiments_name.append(self._project_lib.experimental_data_for_model_at_index().name)
        except IndexError:
            pass
        return experiments_name

    def current_index(self) -> int:
        return self._current_index

    def set_current_index(self, new_value: int) -> None:
        if new_value != self._current_index:
            new_value = self._current_index
            print(new_value)
            return True
        return False
