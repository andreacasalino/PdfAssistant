import os
import re

from pypdf import PdfWriter, PdfReader
from argparse import ArgumentParser

def _for_each_file_in_dir(dir, ext):    
    for d in os.listdir(dir):
        if d.endswith('.{}'.format(ext)):
            yield os.path.join(dir, d)

def _gather_pdf_from_dir(dir):    
    return sorted(_for_each_file_in_dir(dir, 'pdf'))

def _merge(docs_iter, out):
    if not out:
        raise Exception("--out was not specified!")
    
    merger = PdfWriter()
    for pdf in docs_iter:
        print("-- merging {}".format(pdf))
        merger.append(pdf)
    merger.write(out)
    merger.close()

def _parse_range(val):
    if re.compile(r'^\d+,\d+$').match(val):
        sep = val.find(',')
        return int(val[:sep]), int(val[(sep+1):])

    if re.compile(r'^\d+$').match(val):
        return int(val), None
        
    raise Exception("Invalid range of pages")

def _extract_page_range(src_path, out, begin, end = None):
    if not out:
        raise Exception("--out was not specified!")
    
    reader = PdfReader(src_path)
    num_pages = len(reader.pages)

    if not end:
        end = num_pages + 1

    if (begin < 0 or 
        end < 0 or 
        end <= begin or
        not end <= (num_pages + 1)):
        raise Exception("Invalid positions")
    
    begin -= 1
    end -= 1

    print("-- extracting [{}, {}) from {}".format(begin+1, end+1, src_path))

    writer = PdfWriter()
    for page_num in range(begin, end):
        writer.add_page(reader.pages[page_num])
    writer.write(out)
    writer.close()

def main(args):
    if args.merge:
        _merge(args.merge.split(','), args.out)
    elif args.merge_dir:
        pdfs = _gather_pdf_from_dir(args.merge_dir)
        _merge(pdfs, args.out)
    elif args.range:
        begin, end = _parse_range(args.range)
        _extract_page_range(args.doc, args.out, begin, end)

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("--out", default=None, help="The document to create")

    parser.add_argument("--doc", default=None, help="The document to use as source when using '--range'")
    parser.add_argument("--range", default=None, help="syntax is 'begin,end' or just the 'begin' page (all pages after will be taken). This will extract the range [begin, end) (end is exclusive) from the doc specified with option '--doc'")

    parser.add_argument("--merge", default=None, help="comma separated list of docs to merge. The specified order will be assumed for merging")
    parser.add_argument("--merge_dir", default=None, help="specify a directory from which the pages to merge are taken. Alphabetical order is assumed for merging")

    args = parser.parse_args()

    main(args)
