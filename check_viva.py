##############################
# This script checks the thesis-folder on the viva-drive for
# - existance of the thesis-file
# - existance of the assessment-file
##############################

import argparse
import sys

from pathlib import Path
from pypdf import PdfReader
from tqdm import tqdm

viva_path = "\\\\home-pc.uni-bayreuth.de\\group\\vivaorg_18021580\\KT\\Abschlussarbeiten\\"
viva_path = Path(viva_path)

def get_student_name(student):
    s = str(student)
    split = s.rfind("\\")
    return s[split + 1:] if split != 1 else s


def check_for_thesis (path):
    # open path/Arbeit
    path = path / "Arbeit"

    # get all .pdf files
    pdfs = list(path.glob('*.pdf'))

    # return if one has more that 10 pages
    for pdf in pdfs:
        try:
            reader = PdfReader(str(pdf))
            if len(reader.pages) > 10:
                return True
        except:
            print(f"error reading file { str(pdf) }", file=sys.stderr)
        
    return False


def check_for_assessment (path):
    # open path/Arbeit
    path = path / "Gutachten"

    # get all .pdf files
    pdfs = list(path.glob('*.pdf'))

    # return if one has more that 10 pages
    for pdf in pdfs:
        try:
            reader = PdfReader(str(pdf))
            if len(reader.pages) < 10:
                return True
        except:
            print(f"error reading file { str(pdf) }", file=sys.stderr)

    return False


def iter_students (path, exists, check):
    print("Searching students...", file=sys.stderr, end=None)
    students = [x for x in path.iterdir() if x.is_dir()]
    print(" done", file=sys.stderr)

    print(f"Analyzing {len(students)} students...", file=sys.stderr)

    for student in tqdm(students):
        if exists == check(student):
            print(get_student_name(student))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Viva-drive checker.')
    parser.add_argument('--arbeit', dest='arbeit', action='store_true')
    parser.add_argument('--gutachten', dest='gutachten', action='store_true')
    parser.add_argument('--existiert', dest='existiert', action='store_true')
    parser.add_argument(dest='subfolder', action='store', type=str)
    args = parser.parse_args()

    viva_path /= args.subfolder

    if args.existiert:
        exist = ""
    else:
        exist = " nicht"

    if args.arbeit and not args.gutachten:
        doc = "Arbeiten"
    elif not args.arbeit and args.gutachten:
        doc = "Gutachten"
    else:
        parser.print_help()

    print(f"Suche nach{exist} existierenden {doc} im Ordner {args.subfolder}.", file=sys.stderr)

    if args.arbeit:
        iter_students(viva_path, args.existiert, check_for_thesis)
    if args.gutachten:
        iter_students(viva_path, args.existiert, check_for_assessment)

