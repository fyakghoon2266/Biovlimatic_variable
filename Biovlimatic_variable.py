import pandas as pd

class ClimateDataProcessor:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)
        self.process_data()

    def process_data(self):
        self._rename_columns()
        self._convert_schema()

    def _rename_columns(self):
        self.data.rename(columns={
            'temperature_2m_MEAN': 'Temp',
            'temperature_2m_max_MEAN': 'Tmax',
            'temperature_2m_min_MEAN': 'Tmin',
            'total_precipitation_sum_MEAN': 'Prec',
            'STATE':'ID'
        }, inplace=True)

    def _convert_schema(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['Month'] = self.data['Date'].dt.month
        self.data['Year'] = self.data['Date'].dt.year

    def calculate_monthly_data(self):
        self.monthly_data = self.data.groupby(['ID', 'Year', 'Month']).agg({
            'Temp': 'mean',
            'Tmin': 'min',
            'Tmax': 'max',
            'Prec': 'sum'
        }).reset_index()
        self.calculate_bioclimatic_variables()

    def calculate_bioclimatic_variables(self):
        # Annual temperature range
        # bio01: Average annual temperature
        self.monthly_data['Bio01'] = self.monthly_data['Temp']

        # bio02: Annual temperature range (maximum temperature of the year minus minimum temperature of the year)
        self.monthly_data['Bio02'] = self.monthly_data['Tmax'] - self.monthly_data['Tmin']

        # bio04: Isothermality index (annual variation of temperature, standard deviation of the highest and lowest temperatures of the year)
        yearly_temperatures = self.data.groupby(['ID', 'Year'])['Temp'].agg('std').reset_index()
        self.monthly_data = pd.merge(self.monthly_data, yearly_temperatures, on=['ID', 'Year'], suffixes=('', '_std'))
        self.monthly_data['Bio04'] = self.monthly_data['Temp_std']

        # bio05: Highest temperature of the warmest month
        max_temp_warmest_month = self.monthly_data.groupby(['ID', 'Year'])['Tmax'].max().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, max_temp_warmest_month, on=['ID', 'Year'], suffixes=('', '_max_warm'))
        self.monthly_data['Bio05'] = self.monthly_data['Tmax_max_warm']

        # bio06: Lowest temperature of the coldest month
        max_temp_warmest_month = self.monthly_data.groupby(['ID', 'Year'])['Tmin'].min().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, max_temp_warmest_month, on=['ID', 'Year'], suffixes=('', '_min_warm'))
        self.monthly_data['Bio06'] = self.monthly_data['Tmin_min_warm']


        # bio07: Annual temperature difference
        self.monthly_data['Bio07'] = self.monthly_data['Bio05'] - self.monthly_data['Bio06']


        # bio03: Isothermality (constant temperature measure)
        self.monthly_data['Bio03'] = (self.monthly_data['Bio02'] / self.monthly_data['Bio07']) * 100


        # bio08: Average temperature for the month with the highest cumulative precipitation over 3 consecutive months
        # First calculate the cumulative precipitation for each month
        self.monthly_data['cumulative_precipitation'] = self.monthly_data.groupby(['ID', 'Year'])['Prec'].cumsum()

        # Find the month with the highest cumulative precipitation over 3 consecutive months
        max_rain_month = self.monthly_data.groupby(['ID', 'Year'])['cumulative_precipitation'].rolling(window=3).max().reset_index()

        # Add the average temperature of the month with the highest precipitation to the data
        self.monthly_data['Bio08'] = max_rain_month['cumulative_precipitation']

        # bio09: Average temperature of the driest quarter
        # Find the month with the least cumulative precipitation over 3 consecutive months
        min_rain_month = self.monthly_data.groupby(['ID', 'Year'])['cumulative_precipitation'].rolling(window=3).min().reset_index()

        # Add the average temperature of the driest month to the data
        self.monthly_data['Bio09'] = min_rain_month['cumulative_precipitation']

        # bio10: Average temperature of the warmest quarter
        # Find the month with the highest average temperature over 3 consecutive months
        max_temp_quarter = self.monthly_data.groupby(['ID', 'Year'])['Temp'].rolling(window=3).max().reset_index()

        # Add the average temperature of the warmest month to the data
        self.monthly_data['Bio10'] = max_temp_quarter['Temp']

        # bio11: Average temperature of the coldest quarter
        # Find the month with the lowest average temperature over 3 consecutive months
        min_temp_quarter = self.monthly_data.groupby(['ID', 'Year'])['Temp'].rolling(window=3).min().reset_index()

        # Add the average temperature of the coldest month to the data
        self.monthly_data['Bio11'] = min_temp_quarter['Temp']

        # bio12: Annual precipitation
        annual_precipitation = self.data.groupby(['ID', 'Year'])['Prec'].sum().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, annual_precipitation, on=['ID', 'Year'], suffixes=('', '_annual_precipitation'))
        self.monthly_data['Bio12'] = self.monthly_data['Prec_annual_precipitation']

        # bio13: Precipitation of the wettest month
        max_precipitation_wettest_month = self.monthly_data.groupby(['ID', 'Year'])['Prec'].max().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, max_precipitation_wettest_month, on=['ID', 'Year'], suffixes=('', '_max_precipitation_wettest_month'))
        self.monthly_data['Bio13'] = self.monthly_data['Prec_max_precipitation_wettest_month']

        # bio14: Precipitation in driest month
        min_precipitation_driest_month = self.monthly_data.groupby(['ID', 'Year'])['Prec'].min().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, min_precipitation_driest_month, on=['ID', 'Year'], suffixes=('', '_min_precipitation_driest_month'))
        self.monthly_data['Bio14'] = self.monthly_data['Prec_min_precipitation_driest_month']

        # bio15: Precipitation Seasonality
        precipitation_seasonality = self.data.groupby(['ID', 'Year'])['Prec'].std() / self.data.groupby(['ID', 'Year'])['Prec'].mean() * 100
        precipitation_seasonality = precipitation_seasonality.reset_index(name='Bio15')
        self.monthly_data = pd.merge(self.monthly_data, precipitation_seasonality, on=['ID', 'Year'])

        # bio16: Precipitation during the wettest quarter
        max_precipitation_wettest_quarter = self.monthly_data.groupby(['ID', 'Year'])['Prec'].rolling(window=3).sum().groupby(['ID', 'Year']).max().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, max_precipitation_wettest_quarter, on=['ID', 'Year'], suffixes=('', '_max_precipitation_wettest_quarter'))
        self.monthly_data['Bio16'] = self.monthly_data['Prec_max_precipitation_wettest_quarter']

        # bio17: Precipitation during the driest quarter
        min_precipitation_driest_quarter = self.monthly_data.groupby(['ID', 'Year'])['Prec'].rolling(window=3).sum().groupby(['ID', 'Year']).min().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, min_precipitation_driest_quarter, on=['ID', 'Year'], suffixes=('', '_min_precipitation_driest_quarter'))
        self.monthly_data['Bio17'] = self.monthly_data['Prec_min_precipitation_driest_quarter']

        # bio18: Precipitation during the warmest quarter
        max_precipitation_warmest_quarter = self.monthly_data.groupby(['ID', 'Year'])['Prec'].rolling(window=3).sum().groupby(['ID', 'Year']).max().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, max_precipitation_warmest_quarter, on=['ID', 'Year'], suffixes=('', '_max_precipitation_warmest_quarter'))
        self.monthly_data['Bio18'] = self.monthly_data['Prec_max_precipitation_warmest_quarter']

        # bio19: Precipitation during the coldest quarter
        min_precipitation_coldest_quarter = self.monthly_data.groupby(['ID', 'Year'])['Prec'].rolling(window=3).sum().groupby(['ID', 'Year']).min().reset_index()
        self.monthly_data = pd.merge(self.monthly_data, min_precipitation_coldest_quarter, on=['ID', 'Year'], suffixes=('', '_min_precipitation_coldest_quarter'))
        self.monthly_data['Bio19'] = self.monthly_data['Prec_min_precipitation_coldest_quarter']

    def export_data(self, filename):
        select_columns = ['ID', 
                        'Year', 
                        'Temp', 
                        'Tmax', 
                        'Tmin',
                        'Bio01',
                        'Bio02',
                        'Bio03',
                        'Bio04',
                        'Bio05',
                        'Bio06',
                        'Bio07',
                        'Bio08',
                        'Bio09',
                        'Bio10',
                        'Bio11',
                        'Bio12',
                        'Bio13',
                        'Bio14',
                        'Bio15',
                        'Bio16',
                        'Bio17',
                        'Bio18',
                        'Bio19']
        self.monthly_data[select_columns].to_csv(filename, header=True, index=False)
        print(f"Data exported to {filename}")

# Usage example
processor = ClimateDataProcessor('data.csv')
processor.calculate_monthly_data()
processor.export_data('Bio_variable_test.csv')