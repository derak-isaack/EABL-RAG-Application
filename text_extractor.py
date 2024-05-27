import pymupdf
import pymupdf4llm

doc = pymupdf.open("2023-EABL-Annual-Report.pdf") # open a document
out = open("EABL.txt", "wb") # create a text output
for page in doc: # iterate the document pages
    text = page.get_text().replace('\n', ' ')
    text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
    out.write(text) # write text of page
    out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
out.close()

