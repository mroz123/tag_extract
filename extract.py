import sys
from pathlib import Path
import json
import fitz
import re

def openfile(path_to_pdf_file):
    regex = "X_(.*)"
    with fitz.open(path_to_pdf_file) as document:
        out = []
        for pnum, page in enumerate(document):
            final_list = []
            #wlist = page.get_text("json")
            full_dict = page.get_text("dict")

            for b in full_dict["blocks"]:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            if re.match(regex, s["text"]):
                                text = {"text": s["text"]}
                                coor = {
                                    "x":s["origin"][0],
                                    "y":s["origin"][1]}

                                final_list.append({
                                    "tag": s["text"],
                                    "x": s["origin"][0],
                                    "y": s["origin"][1]
                                })
            page_num = {"page_num": pnum}
            width = {"width": full_dict["width"]}
            height = {"height": full_dict["height"]}
            pg = {
                "number": pnum,
                "height": full_dict["height"],
                "width": full_dict["width"],
                "tags": final_list
            }
            out.append(pg)

    return json.dumps(out)

def main():
    if len(sys.argv) > 1:
        print(openfile(Path(sys.argv[1])))
    else:
        print(f"Usage:\vpython3 {sys.argv[0]} <file.pdf>")
        exit(2)

main()

# jq '.blocks[].lines[].spans[] | select(.text |test("XT-(.*)"))' full.json
