import importlib
import re
from glob import glob
from columnar import columnar


class DataDriverManager:
    drivers: list = []

    driver = None

    def __init__(self, driver_to_load: str = "*"):
        self.load(driver_to_load)

    def load(self, driver_to_load: str = "*"):
        for driver_file in glob("./dataDriver/" + driver_to_load + ".py"):
            if "DataDriverExample.py" not in driver_file:
                driver_file = driver_file.replace("\\", "/")  # avoid windows directory cheat
                driver_name = re.sub("\./dataDriver/|\.py", "", driver_file)
                module = importlib.import_module("dataDriver." + driver_name, ".")

                obj = module.Driver()
                obj_content = dir(obj)
                # todo check if contain all value require
                if driver_to_load == "*":
                    self.drivers.append(obj)
                else:
                    self.driver = obj

    def reload(self, driver_to_load: str = "*"):
        self.drivers = []
        self.load(driver_to_load)

    def get_driver(self):
        return self.driver

    def print_available_drivers(self):
        col_headers = ['name', 'author', 'description']

        col_data = []

        for driver in self.drivers:
            col_data.append([
                driver.name,
                driver.author,
                driver.description
            ])

        print(columnar(col_data, col_headers, no_borders=True))
