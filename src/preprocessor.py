import csv

class CSVData:

    _column_list = []

    def __init__(self, file_path):
        """
        Initializes the CSVData object and loads the data from the CSV file.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path
        self.data = self._load_data()
        self._column_list = self.data[0].keys() if self.data else []

    def _load_data(self):
        """
        Private method to load data from the CSV file.

        Returns:
            list: A list of dictionaries where each dictionary represents a row in the CSV.
        """
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def get_row(self, index):
        """
        Gets a specific row by index.

        Args:
            index (int): The index of the row to retrieve.

        Returns:
            dict: The row as a dictionary.
        """
        if 0 <= index < len(self.data):
            return self.data[index]
        else:
            raise IndexError("Row index out of range.")

    def get_column(self, column_name):
        """
        Gets all values from a specific column.

        Args:
            column_name (str): The name of the column to retrieve.

        Returns:
            list: A list of values from the specified column.
        """
        if column_name in self.data[0]:
            return [row[column_name] for row in self.data]
        else:
            raise KeyError(f"Column '{column_name}' does not exist.")

    def get_value(self, index, column_name):
        """
        Gets a specific value by row index and column name.

        Args:
            index (int): The index of the row.
            column_name (str): The name of the column.

        Returns:
            str: The value at the specified row and column.
        """
        row = self.get_row(index)
        if column_name in row:
            return row[column_name]
        else:
            raise KeyError(f"Column '{column_name}' does not exist.")
    
    def size(self):
        """
        Gets the number of rows in the CSV data.

        Returns:
            int: The number of rows.
        """
        return len(self.data)
    
    def list_rows(self):
        """
        Lists all rows in the CSV data.

        Returns:
            list: A list of all rows.
        """
        return self._column_list
