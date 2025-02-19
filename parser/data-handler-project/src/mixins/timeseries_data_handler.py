class TimeseriesDataHandler:
    """
    Mixin class for handling timeseries data.

    This mixin provides methods for processing timeseries data, where each data point includes a time component.
    """

    def __init__(self):
        self.timeseries_data = []

    def load_timeseries_data(self, data):
        """
        Load timeseries data from a given source.

        Args:
            data (list): A list of tuples or lists where each entry contains a timestamp and a corresponding value.
        """
        self.timeseries_data = data

    def get_timeseries_values(self):
        """
        Retrieve the values from the timeseries data.

        Returns:
            list: A list of values corresponding to the timeseries data.
        """
        return [value for timestamp, value in self.timeseries_data]

    def get_timeseries_timestamps(self):
        """
        Retrieve the timestamps from the timeseries data.

        Returns:
            list: A list of timestamps corresponding to the timeseries data.
        """
        return [timestamp for timestamp, value in self.timeseries_data]