## INTRO

Have you ever needed to merge **pdf** files or extract pages from them? 
Certainly you have wasted hours finding a tool for that. Maybe you have used an online tool, requiring to upload confidential documents.

Well ... that time is over now! With the [main.py](./main.py) script contained in this repo you can easily manipulate **pdf** locally with no stress.

## PREREQUISITES

[main.py](./main.py) needs [**python**](https://www.python.org/) to be installed on your system as well as the [**pypdf**](https://pypi.org/project/pypdf/) package. Nothing else is required.

## MERGE

Just run:
```bash
python3 main.py --out the_result_file.pdf --merge 'first_file_path.pdf,second_file_path.pdf,third_file_path.pdf'
```
the out path as well as each specified file to merge, can be also relative or absolute paths to the actual files.

Alternatively, you may want to merge all files in a certain directory:
```bash
python3 main.py --out the_result_file.pdf --merge_dir the_directory_with_all_files_to_merge
```

## EXTRACT

If you want to extract the pages in the range 6..9, with 6 included and 9 excluded, from a source **pdf** file just run:
```bash
python3 main.py --out the_result_file.pdf --doc the_source_file.pdf --range '6,9'
```
