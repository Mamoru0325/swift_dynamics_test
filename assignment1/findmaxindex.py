class FindMaxValueIndex:
    """
    This class will use to find an index of max value in array
        :argument:
            arr (list): List of int to find max value
    """
    def __init__(self, arr):
        self._arr = arr

    @property
    def arr(self):
        """
        Getter Method
        """
        return self._arr

    @arr.setter
    def arr(self, arr):
        """
        Setter Method
        """
        if isinstance(arr, list):
            checkdigit = 1  # check counter to correct every item in list is int
            for item in arr:
                if not item.isdigit():
                    checkdigit = 0
            if checkdigit:
                self._arr = arr
        else:
            raise TypeError('This value is not a list type')

    def find_max_value_index(self):
        """
        This method use to find max value from list
            :return:
                index (int): Index of max value
        """
        index = 0
        max_value = self.arr[index]
        for item in self.arr:
            if max_value <= item:
                max_value = item
                index = self.arr.index(max_value)
        return index


if __name__ == "__main__":
    """
    Array that insert will in this format 'X X X X' 
    PS. X is integer in array  
    """
    sentence = "Please insert array to find index: "
    arr = list(map(int, input(sentence).split()))
    index = FindMaxValueIndex(arr)
    result = f'The index of max value is {index.find_max_value_index()}'
    print(result)
