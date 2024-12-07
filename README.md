# ECE143 Group 11 Final Project
# UCSD Bike & Scooter Theft Analysis


- **Problem Statement**: _Where and why do bikes and scooters get stolen on the UCSD campus?_
\
Understanding the factors contributing to these incidents can help develop preventive measures.
- **Dataset**: We analyzed the UCSD Police reports to assess theft likelihood based on factors like location, time, cost, and weather conditions. We developed scripts to harvest daily police reports from [UCSD Police Reports](https://www.police.ucsd.edu/docs/reports/callsandarrests/Calls_and_Arrests.asp) and parsed them into meaningful data points.
- **Our Solution**: Our solution to the problem statement involves creating a dataset of bike and scooter thefts based on police reports. Using this data, we analyzed the patterns and predicted theft likelihood based on multiple conditions. Additionally, visualizations help highlight trends, such as locations with high theft rates, peak times for incidents, and cost distribution.
- **Real-World Application**: This solution can be practically applied to improve campus security and inform students about safe locations and times for parking their bikes. UCSD authorities can use these insights to focus resources on high-risk areas or times, potentially reducing the frequency of theft.


---

Our project is hosted on [Streamlit](https://ece143project.streamlit.app/). It is an interactive webapp presenting our analysis and observations in an intituitive graphical way. Check it out!

---

**Our Team**
- Mingwei Yeoh ()
- Parjanya Prashant (A15778224)
- Pranav Raj (A59026510)
- Wendeng Wang (A69036364)
- Yash Jain (A59026285)

---

**Requirements**

- python>=3.9
- pandas==2.2.0
- numpy==1.26.4
- requests==2.31.0
- tqdm==4.66.2

---

### Running Streamlit Locally

To run the application locally using Streamlit, execute the following command:
```bash
streamlit run main.py
```

---

### Brief Overview of Datasets

- **mingextract.csv**: This file contains the extracted crime data.

- **mingextract_with_weather.csv**: This file contains the extracted crime data + the weather (temperature and precipitation) data at UCSD for the date and time of the crime.

- **random_weather_data.csv**: This file contains the weather data at UCSD for random timestamps.

- **time_type_proportions.csv**: This file contains the proportions of different classes of stolen items accross different time periods in the day.

###  Brief Overview of Files



- **main.py**: This file contains the code responsible for rendering the front end. When needed, it calls functions from **functions.py** to process data and generate a pandas DataFrame for front-end display.

- **functions.py**: This file contains utility functions used by **main.py** to process and manipulate data, including generating data frames for graphing.

- **analysis.ipynb**: This jupyter notebook contains the code we used to analyse the dataset and generate relevant presentation graphs.

- **weather_analysis.ipynb**: This jupyter notebook contains the code we used to analyse the dataset and generate relevant presentation graphs for the weather data.

- **/PDFExtraction**: This folder contains the scripts for extracting data from the PDF files in **/Resources**. The extracted data is stored in a CSV file. This process only needs to be run once to populate the dataset.

- **/classifier**: This folder has the code to implement a Random-forest classifier to generate a predicted heatmap of thefts.

- **weather/get_weather.py**: Obtaines weather data (temperature and precipitation) at UCSD for the timestamps of crimes.

