# -*- coding: utf-8 -*-
import os

TEMPLATE_FOLDER = "template"
STATIC_FOLDER = "static"


class FolderError(Exception):
    __slots__ = ['msg']

    def __init__(self, msg='folder not find'):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileError(Exception):
    __slots__ = ['msg']

    def __init__(self, msg='File not find'):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileImp:
    __slots__ = ["folder_path", "file_name", "default_path"]

    def __init__(self, default_path,
                 folder_path,
                 file_name):
        self.folder_path = folder_path
        self.file_name = file_name
        self.default_path = default_path

    def __repr__(self):
        return "{} {} {}".format(self.default_path, self.folder_path, self.file_name)

    def exist_folder(self) -> bool:
        return os.path.isdir(os.path.join(self.default_path, self.folder_path))

    def exist_file(self) -> bool:
        return os.path.exists(os.path.join(self.default_path, self.folder_path, self.file_name))

    def read_file(self) -> str:
        file_path = os.path.join(self.default_path, self.folder_path, self.file_name)
        with open(file_path, encoding='utf8') as f:
            contents = f.read()
            return contents


# TODO 템플릿 언어 적용
class RenderHandler(FileImp):
    def __init__(self, folder_path: str, file_name: str):
        super().__init__(TEMPLATE_FOLDER, folder_path, file_name)

    def __call__(self, *args, **kwargs):

        if self.exist_folder() is False:
            raise FolderError

        if self.exist_file() is False:
            raise FileError

        return self.read_file()


class StaticFileHandler(FileImp):
    def __init__(self, folder_path: str, file_name: str):
        super().__init__(STATIC_FOLDER, folder_path, file_name)

    def __call__(self, *args, **kwargs):

        if self.exist_folder() is False:
            raise FolderError

        if self.exist_file() is False:
            raise FileError

        if self.file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            return self.read_image_file()
        else:
            return self.read_file()

    def read_image_file(self) -> str:
        file_path = os.path.join(self.default_path, self.folder_path, self.file_name)
        stream = open(file_path, "rb")
        return stream.read()
