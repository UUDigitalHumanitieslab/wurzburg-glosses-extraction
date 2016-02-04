# Würzburg glosses extraction

Allows one to extract grammatical information on glosses from the Würzburg glosses lexicon (Kavanagh 2001).

## Usage

Starting from the PDF version of the lexicon, one can use `pdf2html.py` to convert to HTML 
(uses [PDFMiner](https://euske.github.io/pdfminer/)), 
and then `cleanhtml.py` to remove tags (uses [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)). 

After preprocessing, `run.py` allows one to extract grammatical information out of the lexicon. 

### Web application

This project comes with a small web application (build in [Flask](http://flask.pocoo.org/)) that allows you to
run the extraction for a single gloss, in case something went wrong during the automatic phase. The web application
can be started by running `web.py`. 

## References

Kavanagh, Seamus (2001).
*A lexicon of the Old Irish glosses in the Würzburg Manuscript of the Epistles of St. Paul.* 
Edited by Dagmar S. Wodtko.
Österreichische Akademie der Wissenschaften.
