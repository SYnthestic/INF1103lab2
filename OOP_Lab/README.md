Build Docker: docker build -t inf1103-labs-smart-auditor .
Run Docker: docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor

UMD Diagram: pyreverse -o png -p OOP_Lab_UML (Get-ChildItem -Recurse -Filter *.py | Where-Object { $_.FullName -notmatch '\\\.venv\\' } | Resolve-Path -Relative)   