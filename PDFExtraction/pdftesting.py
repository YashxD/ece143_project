from pdftocsv import PDFanalyzer
from pathlib import Path 
import csv


with open("mingextract.csv", mode='w', newline='') as file: # Clear the data file
  writer = csv.writer(file)

# UCSDday = PDFanalyzer("Resources/2023/07.2023 July.pdf", 104, 105)

# Recursively iterate through all files
for file_path in Path("Resources").rglob("*.pdf"):
  if file_path.is_file():  # Ensure it's a file
    print(file_path)
    UCSDday = PDFanalyzer(file_path, 0, -1)
