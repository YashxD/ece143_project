# ECE143 Group 11 Final Project
# UCSD Bike & Scooter Theft Analysis

### Running Streamlit Locally

To run the application locally using Streamlit, execute the following command:
```bash
streamlit run main.py
```

###  Brief Overview of Files

- **main.py**: This file contains the code responsible for rendering the front end. When needed, it calls functions from **functions.py** to process data and generate a pandas DataFrame for front-end display.

- **functions.py**: This file contains utility functions used by **main.py** to process and manipulate data, including generating data frames for graphing.

- **/PDFExtraction**: This folder contains the scripts for extracting data from the PDF files in **/Resources**. The extracted data is stored in a CSV file. This process only needs to be run once to populate the dataset.

- **/classifier**:This folder has the code to implement a Random-forest classifier to generate a predicted heatmap of thefts.
