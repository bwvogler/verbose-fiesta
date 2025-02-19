# FILE: /data-handler-project/data-handler-project/src/main.py
from mixins.csv_handler import CSVHandler
from mixins.excel_handler import ExcelHandler
from mixins.spectral_data_handler import SpectralDataHandler
from mixins.timeseries_data_handler import TimeseriesDataHandler

class DataHandler(CSVHandler, ExcelHandler, SpectralDataHandler, TimeseriesDataHandler):
    """
    DataHandler class that composes mixins for handling different data formats and types.
    This class ensures mutual exclusivity between CSV and Excel formats.
    """

    def __init__(self, data_source, data_type):
        self.data_source = data_source
        self.data_type = data_type

    def load_data(self):
        if self.data_source.endswith('.csv'):
            return self.read_csv(self.data_source)
        elif self.data_source.endswith(('.xls', '.xlsx')):
            return self.read_excel(self.data_source)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    def process_data(self):
        if self.data_type == 'spectral':
            return self.handle_spectral_data()
        elif self.data_type == 'timeseries':
            return self.handle_timeseries_data()
        else:
            raise ValueError("Unsupported data type. Please specify 'spectral' or 'timeseries'.")

if __name__ == "__main__":
    # Example usage
    data_handler = DataHandler('data.csv', 'spectral')
    data = data_handler.load_data()
    processed_data = data_handler.process_data()
    print(processed_data)