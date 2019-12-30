# -*- coding: utf-8 -*-

class HomesAPI:
    @staticmethod
    def do_index(request):
        return "<html><head><meta charset='UTF-8' /></head><body>english 한글 </body></html>"

    @staticmethod
    def do_create():
        print("home do_create")
