class MospiError(Exception):
    """Base exception for mospi package."""


class InvalidDatasetError(MospiError):
    """Raised when an invalid dataset name is provided."""

    def __init__(self, dataset: str, valid_datasets: list, suggestions: list = None):
        self.dataset = dataset
        self.valid_datasets = valid_datasets
        self.suggestions = suggestions or []
        msg = f"Unknown dataset: '{dataset}'. Valid datasets: {', '.join(valid_datasets)}"
        if self.suggestions:
            msg += f". Did you mean: {', '.join(self.suggestions)}?"
        super().__init__(msg)


class InvalidFilterError(MospiError):
    """Raised when invalid filter parameters are provided."""

    def __init__(self, message: str, invalid_params: list = None, valid_params: list = None):
        self.invalid_params = invalid_params
        self.valid_params = valid_params
        super().__init__(message)


class APIError(MospiError):
    """Raised when the MoSPI API returns an error."""

    def __init__(
        self,
        message: str,
        dataset: str = None,
        filters: dict = None,
        troubleshooting: str = None,
        suggestion: str = None,
        response: dict = None,
    ):
        self.dataset = dataset
        self.filters = filters
        self.troubleshooting = troubleshooting
        self.suggestion = suggestion
        self.response = response
        super().__init__(message)


class NoDataError(MospiError):
    """Raised when the API returns a valid response with no matching records."""

    def __init__(
        self,
        message: str,
        dataset: str = None,
        filters: dict = None,
        troubleshooting: str = None,
        suggestion: str = None,
        response: dict = None,
    ):
        self.dataset = dataset
        self.filters = filters
        self.troubleshooting = troubleshooting
        self.suggestion = suggestion
        self.response = response
        super().__init__(message)
