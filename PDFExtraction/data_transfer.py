import os
import pdfplumber
import pandas as pd
import numpy as np

# # Initialize a dictionary to store data
data = {
    "Date Reported": [],
    "Date Occurred": [],
    "Time Occurred": [],
    "Incident Type": [],
    "Location": [],
    "Incident/Case#": [],
    "Summary": [],
    "Disposition": []
}


def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')[3:]  # skip the first 3 line(title useless information)
                event_data = {}
                in_summary = False

                i=0

                for line in lines:
                    line = line.strip()

                    # the four line is "Incident Type"
                    if i == 0:
                        event_data["Incident Type"] = line
                    # five line is "Location"
                    elif i == 1:
                        event_data["Location"] = line

                    # if line.startswith("Incident Type"):
                    #     event_data["Incident Type"] = line.replace("Incident Type", "").strip()
                    # elif line.startswith("Location"):
                    #     event_data["Location"] = line.replace("Location", "").strip()
                    elif line.startswith("Date Reported"):
                        event_data["Date Reported"] = line.replace("Date Reported", "").strip()
                    elif line.startswith("Incident/Case#"):
                        event_data["Incident/Case#"] = line.replace("Incident/Case#", "").strip()
                    elif line.startswith("Date Occurred"):
                        event_data["Date Occurred"] = line.replace("Date Occurred", "").strip()
                    elif line.startswith("Time Occurred"):
                        event_data["Time Occurred"] = line.replace("Time Occurred", "").strip()
                    elif line.startswith("Summary:"):
                        # start collecting Summary
                        event_data["Summary"] = line.replace("Summary:", "").strip()
                        in_summary = True
                    elif line.startswith("Disposition"):
                        # stop collecting Summary  and start collecting Disposition
                        in_summary = False
                        event_data["Disposition"] = line.replace("Disposition:", "").strip()

                        # reset event_data
                        for key in data.keys():
                            data[key].append(event_data.get(key, np.nan))
                        event_data = {}
                        i=-1
                    elif in_summary:
                        # the summary sometimes has more than one line
                        event_data["Summary"] += " " + line.strip()

                    i+=1





root_directory = 'C:/Users/Wander/Desktop/dataset/UCPD 2019-2024'
for root, dirs, files in os.walk(root_directory):
    count=0
    for file in files:
        count+=1
        print(count)
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            extract_data_from_pdf(pdf_path)


df = pd.DataFrame(data)
output_csv_path = 'data_transfer.csv'
df.to_csv(output_csv_path, index=False)

print(f"Data has been saved to {output_csv_path}")
