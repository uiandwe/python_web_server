# -*- coding: utf-8 -*-
import os

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


class RenderHandler:
    __slots__ = ["class_name", "file_name"]
    TEMPLATE_FOLDER = "template"

    def __init__(self, class_name, file_name):
        self.class_name = class_name
        self.file_name = file_name

    def __call__(self, *args, **kwargs):

        if self.exist_folder() is False:
            raise FolderError

        if self.exist_file() is False:
            raise FileError

        return self.file_read()

    def __repr__(self):
        return "{} {}".format(self.class_name, self.file_name)

    def exist_folder(self):
        return os.path.isdir(os.path.join(RenderHandler.TEMPLATE_FOLDER, self.class_name))

    def exist_file(self):
        return os.path.exists(os.path.join(RenderHandler.TEMPLATE_FOLDER, self.class_name, self.file_name))

    def file_read(self):
        file_path = os.path.join(RenderHandler.TEMPLATE_FOLDER, self.class_name, self.file_name)
        with open(file_path, encoding='utf8') as f:
            contents = f.read()
            return contents
