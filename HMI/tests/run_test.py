#from the HMI directory run - python tests/run_test.py

import unittest
from test_file_interpreter import TestFileInterpreter
from test_storage import TestStorage
from test_slicer import TestSlicer


if __name__ == '__main__':
    test_classes_to_run = [TestFileInterpreter,
                           TestStorage, 
                           TestSlicer]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)