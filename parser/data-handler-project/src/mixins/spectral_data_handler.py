class SpectralDataHandler:
    """
    Mixin class for handling spectral data.

    This mixin provides methods for processing one-dimensional wavelength data.
    """

    def read_spectral_data(self, file_path: str) -> None:
        """
        Reads spectral data from a specified file.

        Args:
            file_path (str): The path to the spectral data file.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def process_spectral_data(self, data) -> None:
        """
        Processes the spectral data.

        Args:
            data: The spectral data to process.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def plot_spectral_data(self, data) -> None:
        """
        Plots the spectral data.

        Args:
            data: The spectral data to plot.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")