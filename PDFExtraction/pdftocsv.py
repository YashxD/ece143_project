import pdfplumber
import re
from datetime import datetime
import csv

class PDFanalyzer:
  def __init__(self, filepath, startpage, endpage):
    pdf = pdfplumber.open(filepath)
    self.pageNum = len(pdf.pages)
    if endpage == -1:
      endpage = self.pageNum
    self.dateReportedLines = []
    self.data = []
    self.year = ""
    self.numFormattingErrors = 0
    
    self.text = ""
    for page in range(startpage, endpage):
      self.text = self.text + pdf.pages[page].extract_text()
    
    # with open("data.txt", 'w') as file: # For debugging purposes
    #   for line in self.text:
    #       file.write(line)
    
    self.findLines("Date Reported", self.dateReportedLines)
    self.grabPageInformation()
    print(f"Finished with {self.numFormattingErrors} errors")

  def grabPageInformation(self):
    numEvents = len(self.dateReportedLines)
    
    for i in range (0, numEvents):
      title = self.getLine(self.dateReportedLines[i]-2).lower()
      summary = self.getLine(self.dateReportedLines[i]+4).lower()
      if (title.find("theft") != -1): # Look at the title and search for "theft"        
        vehicle_type = re.findall(r"\b(bicycle|scooter|skateboard)\b", summary + title)
        if (len(vehicle_type) != 0):
          try:
            print(f"Line {self.dateReportedLines[i]-1}")
            
            location = self.fixString(self.getLine(self.dateReportedLines[i]-1)).lower()
            location = re.sub(r"Bike Racks?|Bike|storage|West|East", "", location, flags = re.IGNORECASE) # Sub out these works from the location
            
            price = self.getPrice(summary)
            times = self.getLine(self.dateReportedLines[i]+3).upper()
            
            date_matches = re.findall(r"\d+/\d+/\d+",self.getLine(self.dateReportedLines[i]+2))
            if (len(date_matches) == 0): # Someone just didn't know when their bike got stolen wtf
              date_matches.append(re.findall(r"\d+/\d+/\d+",self.getLine(self.dateReportedLines[i]))[0]) # Just append the date that the call was placed
            
            for index, date_match in enumerate(date_matches): # Fix the number of digits that represents the years. Sometimes there are 2 sometimes 4, one time there were 3??
              year = re.findall(r"\d+$", date_match)[0] 
              if (len(year) == 4):
                self.year = year # Update the year that we are currently in based on the previous reports in the pdf
              else:
                date_matches[index] = re.sub(r"\d+$", self.year, date_match) # Too many year errors, lets manually update the year
              
            
            time_matches = re.findall(r"\d+:\d+\s?[AP]M", times)
            
            
            for index, time_match in enumerate(time_matches): 
              if (len(re.findall(r"\d+:\d+[AP]M", time_match)) != 0): # Add a space in between the MINUTES and PM/AM
                time_matches[index] = re.sub(r"(?<=\d)(AM|PM)", r" \1", time_match)
              if time_match == "00:00 PM": # Sometimes seconds are included, screw it set it to 0
                print("\n\n\n\n\n\n\n\n Time incorrect!!!!!!!!")
                time_matches[index] = "12:00 PM"
            
            if (len(time_matches) == 0): # Sometimes absolutely no time is given
              time_matches.append("12:00 PM") # We'll just assume mid day
            date_end = date_matches[len(date_matches) - 1] # Sometimes the end date is not given
            time_end = time_matches[len(time_matches) - 1] # Sometimes the end time is not given
            
            starttime = datetime.strptime(f"{date_matches[0]} {time_matches[0]}", "%m/%d/%Y %I:%M %p")
            endtime = datetime.strptime(f"{date_end} {time_end}", "%m/%d/%Y %I:%M %p")  
            
            mid_time = starttime + (endtime - starttime) / 2
            
            eventData = {
              "type": vehicle_type[0],
              "price": price,
              "location": location,
              "date": mid_time.strftime("%m/%d/%Y"),
              "time": mid_time.strftime("%H:%M")
            }
            
          
            if eventData not in self.data:  
              with open("mingextract.csv", mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=eventData.keys())
                # Write header only if the file is new or empty
                if file.tell() == 0:  # Check if the file is empty
                  writer.writeheader()
                writer.writerow(eventData)
                
              print(eventData)
              self.data.append(eventData)
            
          except:
            self.numFormattingErrors = self.numFormattingErrors + 1
            print("----- Formatting Error -----")

  def getPrice(self, str):
    regex_price_matches = re.findall("\$(\d+\S+)", str)
    if (len(regex_price_matches)) == 0:
      return -1
    else:
      return re.sub(r",", "", regex_price_matches[0]).split(".")[0]

  def getInfo(self, line, notinclude):
    index = self.getLine(line).find(notinclude) + len(notinclude)
    return self.getLine(line)[index:]

  def fixString(self, string):
    newstring = string.replace("\n", "")
    newstring = newstring.replace("\xa0", " ")
    newstring = newstring.replace("\u2010", "-") # Replace hyphen with a minus sign
    newstring = newstring.strip()
    return newstring

  def findLines(self, text, arr): # Finds lines with given word
    arr.clear()
    for i in range(0 , self.text.count('\n')+1 ):
      curLine = self.getLine(i).find(text)
      if (curLine != -1):
        arr.append(i)

  def getLine(self, line): # Retrieves information in a given line
    count = 0
    lastIndex = 0
    while (line != count):
      lastIndex = self.text.find('\n', lastIndex+1)
      count +=1
    nextIndex = self.text.find('\n', lastIndex+1)
    return self.text[lastIndex : nextIndex]

  
