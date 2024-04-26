# Würzburg glosses extraction

[![DOI](https://zenodo.org/badge/45532188.svg)](https://zenodo.org/doi/10.5281/zenodo.11072622)

Allows one to extract grammatical information on glosses from the Würzburg glosses lexicon (Kavanagh 2001).

## Usage

Starting from the PDF version of the lexicon, one can use `pdf2html.py` to convert to HTML (uses [PDFMiner](https://euske.github.io/pdfminer/)), and then `cleanhtml.py` to remove tags (uses [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)). 

After preprocessing, `run.py` allows one to extract grammatical information out of the lexicon. 

### Web application

This project comes with a small web application (build in [Flask](https://flask.palletsprojects.com)) that allows you to
run the extraction for a single gloss, in case something went wrong during the automatic phase. The web application
can be started by running `web.py`. 

## Licence

This work is shared under a BSD 3-Clause licence. See [LICENSE](./LICENSE) for more information.

## Citation

To cite this repository, please use the metadata provided in [CITATION.cff](./CITATION.cff).

## Contact

Würzburg glosses extraction is developed by Martijn van der Klis and the [Research Software Lab](https://cdh.uu.nl/rsl) at the Centre for Digital Humanities, Utrecht University.

For questions or suggestions, [contact the Centre for Digital Humanities](https://cdh.uu.nl/contact/) or open an issue in this respository.


## References

Kavanagh, Seamus (2001).
*A lexicon of the Old Irish glosses in the Würzburg Manuscript of the Epistles of St. Paul.* 
Edited by Dagmar S. Wodtko.
Österreichische Akademie der Wissenschaften.
