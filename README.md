# Climate Data Processor

## Introduction
This project includes a Python class and a Jupyter Notebook for processing climate data. It is designed to calculate various bioclimatic variables from weather data such as temperature and precipitation.

## Files
- `ClimateDataProcessor.py`: This Python file contains the `ClimateDataProcessor` class used for loading, processing, and exporting climate data.
- `Biovlimatic_variable.ipynb`: A Jupyter Notebook that uses the `ClimateDataProcessor` class to perform data analysis and visualize the results.

## Installation
To run this project, you will need Python installed on your system along with the following libraries:
- pandas

You can install the required libraries using pip:

## Usage
### Using the Python Class
1. Import the class from the Python file.
   ```python
   from ClimateDataProcessor import ClimateDataProcessor
   ```
2. Create an instance of the class by passing the path to your data file.
    ```python
    processor = ClimateDataProcessor('data.csv')
    ```

3. Call the methods to process the data and export the results.

    ```python
    processor.calculate_monthly_data()
    processor.export_data('Bio_variable.csv')
    ```

# Bioclimatic Variable Analysis

## Introduction
This repository contains a Jupyter Notebook (`Biovlimatic_variable.ipynb`) designed to process and analyze climate data. It calculates various bioclimatic indicators using temperature and precipitation data from CSV files.

## Installation
To use this notebook, ensure that you have the following prerequisites installed:
- Python 3.x
- Jupyter Notebook or JupyterLab
- Pandas library

You can install the necessary Python libraries using pip:
```bash
pip install notebook pandas
```

## Usage
To use the notebook:

1. **Open the Notebook**: Launch Jupyter Notebook or JupyterLab and open `Biovlimatic_variable.ipynb`.
2. **Run the Notebook**: Execute the cells in sequence to:
   - Load the climate data from a CSV file.
   - Process the data by renaming columns and converting data types.
   - Calculate bioclimatic variables such as temperature range and precipitation indices.
   - Export the processed data to a CSV file for further analysis.

## Functionality
The notebook facilitates several key functions:

- **Data Loading**: Import climate data from CSV files.
- **Data Processing**: Modify column names for clarity, convert columns to appropriate data types, and compute monthly aggregates.
- **Variable Calculation**: Compute various bioclimatic variables that help in understanding climate patterns.
- **Data Exporting**: Save the processed data into a CSV file, making it easy to share and use in other applications.

## Contributing
Contributions are welcome! If you have suggestions for improving this notebook, please:

1. Fork the repository.
2. Create a new branch for your modifications.
3. Commit your changes.
4. Push to the branch.
5. Submit a pull request.

## License
This project is open-sourced under the MIT License. For more details, please check the LICENSE file in the repository.

