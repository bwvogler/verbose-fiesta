# Data Handler Project

This project provides a set of mixins for handling different input data formats (CSV and Excel) and data types (spectral data and timeseries data). The mixins are designed to be used together while ensuring mutual exclusivity between CSV and Excel formats.

## Project Structure

```
data-handler-project
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── mixins
│   │   ├── __init__.py
│   │   ├── csv_handler.py
│   │   ├── excel_handler.py
│   │   ├── spectral_data_handler.py
│   │   └── timeseries_data_handler.py
├── requirements.txt
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The mixins can be imported and used in your own classes to handle different data formats and types. Here’s a brief overview of each mixin:

- **CSVHandler**: Provides methods for reading and processing CSV files. Ensure that this mixin is not used alongside the ExcelHandler mixin.

- **ExcelHandler**: Provides methods for reading and processing Excel files. Ensure that this mixin is not used alongside the CSVHandler mixin.

- **SpectralDataHandler**: Provides methods for handling spectral data, focusing on one-dimensional wavelength data.

- **TimeseriesDataHandler**: Provides methods for handling timeseries data, where each data point includes a time component.

## Example

Here’s a simple example of how to use the mixins in a class:

```python
from mixins.csv_handler import CSVHandler
from mixins.spectral_data_handler import SpectralDataHandler

class DataProcessor(CSVHandler, SpectralDataHandler):
    def process_data(self, file_path):
        # Implementation for processing data
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.