import unittest
import final_air as fa
filename = 'purple_air.csv'

my_dataset = fa.DataSet()
print(type(fa.DataSet()))


class Tester(unittest.TestCase):

    def test_load_file(self):
        my_dataset.load_file()
        self.assertEqual(6147, len(my_dataset._data))

    def test_object_instance(self):
        self.assertIsInstance(my_dataset, type(fa.DataSet()))


if __name__ == '__main__':
    unittest.main()
r"""
---Sample Run 1---
Testing started at 6:55 PM ...
Launching unittests with arguments python -m unittest C:/Users/tmuza/PycharmProjects/CS3AAssignments/unit_test.py in C:\Users\tmuza\PycharmProjects\CS3AAssignments

<class 'final_air.DataSet'>


Ran 2 tests in 0.011s

OK
6147 lines of data were downloaded

Process finished with exit code 0

"""