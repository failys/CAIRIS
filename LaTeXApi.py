#!/usr/bin/env python
from flask import Flask, request
from cairis.core.armid import *
import os


app = Flask(__name__)


@app.route('/latexApi/fileName/<fileName>', methods=['GET'])
def index(fileName):
    typeFlags = request.args.getlist('typeFlags', type=int)
    docDir = request.args.get('docDir')
    docFile = request.args.get('docFile')

    if (typeFlags[DOCOPT_HTML_ID]):
        htmlGenCmd = 'docbook2html -o ' + docDir + ' ' + docFile
        os.system(htmlGenCmd)
    if (typeFlags[DOCOPT_RTF_ID]):
        rtfGenCmd = 'docbook2rtf -o ' + docDir + ' ' + docFile
        os.system(rtfGenCmd)
    if (typeFlags[DOCOPT_PDF_ID]):
        pdfGenCmd = 'dblatex --param=table.in.float="0" -o  ' + \
            docDir + '/' + fileName + '.pdf ' + docFile
        os.system(pdfGenCmd)
    return 'WOOOOO'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)