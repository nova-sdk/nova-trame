"""Model implementation for DataSelector."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from natsort import natsorted
from pydantic import BaseModel, Field


class DataSelectorState(BaseModel, validate_assignment=True):
    """Selection state for identifying datafiles."""

    directory: str = Field(default="")
    extensions: List[str] = Field(default=[])
    search: str = Field(default="", title="Search")
    subdirectory: str = Field(default="")


class DataSelectorModel:
    """Manages file system interactions for the DataSelector widget."""

    def __init__(self, state: DataSelectorState) -> None:
        self.state: DataSelectorState = state

    def set_binding_parameters(self, **kwargs: Any) -> None:
        if "directory" in kwargs:
            self.state.directory = kwargs["directory"]
        if "extensions" in kwargs:
            self.state.extensions = kwargs["extensions"]
        if "subdirectory" in kwargs:
            self.state.subdirectory = kwargs["subdirectory"]

    def sort_directories(self, directories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return natsorted(directories, key=lambda x: x["title"])

    def get_directories_from_path(self, base_path: Path) -> List[Dict[str, Any]]:
        search_path = os.path.join(self.state.directory, base_path)
        directories = []
        try:
            for entry in os.listdir(search_path):
                entry_path = os.path.join(search_path, entry)
                if os.path.isdir(entry_path):
                    directories.append({"children": [], "path": entry_path, "title": entry})
        except OSError:
            pass

        return self.sort_directories(directories)

    def get_directories(self, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        if base_path:
            pass
        else:
            base_path = Path(self.state.directory)

        if not base_path:
            return []

        return self.get_directories_from_path(base_path)

    def get_datafiles_from_path(self, base_path: Path) -> List[str]:
        datafiles = []
        try:
            datafile_path = base_path / self.state.subdirectory

            for entry in os.scandir(datafile_path):
                can_add = False
                if entry.is_file():
                    if self.state.extensions:
                        for extension in self.state.extensions:
                            if entry.path.lower().endswith(extension):
                                can_add = True
                                break
                    else:
                        can_add = True

                if self.state.search and self.state.search.lower() not in entry.name.lower():
                    can_add = False

                if can_add:
                    datafiles.append(entry.path)
        except OSError:
            pass

        return natsorted(datafiles)

    def get_datafiles(self) -> List[Dict[str, str]]:
        base_path = Path(self.state.directory)

        return [{"path": datafile} for datafile in self.get_datafiles_from_path(base_path)]

    def set_subdirectory(self, subdirectory_path: str) -> None:
        self.state.subdirectory = subdirectory_path
