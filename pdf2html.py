import subprocess
import glob
import os

# Transforms a set of .pdf-files into .txt. 
# Uses the pdf2txt.py script from PDFMiner: https://github.com/euske/pdfminer
for f in glob.glob('data/wurzburg/*.pdf'):
    text_file = os.path.splitext(f)[0] + '.html'
    subprocess.call(['python', 'C:\Python27\Scripts\pdf2txt.py', '-o', text_file, f])
    # TODO: remove page 1 from 'A'
