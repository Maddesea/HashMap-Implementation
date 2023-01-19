# Name: Sean Madden
# OSU Email: maddesea@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: 12/2/2022
# Description: This program implements a hash map and utilizes separate chaining. Separate chaining is a collision resolution technique that uses a linked list to store the values that hash to the same index.
# This method of collision resolution is used to avoid the clustering problem that occurs with open addressing and linear probing. The hash map is implemented using a dynamic array of linked lists (included in their respective classes) provided in a6_include.py.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method (named put) updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value. 
        If the given key does not exist in the hash map, a new key/value pair is added. 
        """
        hash = self._hash_function(key)
        index = hash % self._capacity  # index of bucket in hash map
        if self._buckets[index].contains(key):
            # if key already exists, update value
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value
        else:
            # if key does not exist, add key/value pair
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        This method (named empty_buckets) returns the number of empty buckets in the hash table.
        """
        count = 0
        for i in range(self._capacity):  # iterate through hash map and count empty buckets
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        This method (named table_load) returns the current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        This method (named clear) removes all key/value pairs from the hash map. IT does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()  # create new DynamicArray
        i = 0
        while i < self._capacity:
            # add empty LinkedLists to DynamicArray
            self._buckets.append(LinkedList())
            i += 1
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        This method (named resize_table) changes the capacity of the internal hash table. Al existing key/value pairs remain in the new hash map, and all hash table links must be rehashed. 
        The method first checks if the new_capacity is not less than 1; if it is, the method does nothing but if new_capacity is 1 or greater, the method resizes the hash table to the next prime number greater than or equal to new_capacity.
        """
        old_capacity = self._capacity  # save old capacity to iterate through old hash map
        temp = DynamicArray()
        for i in range(old_capacity):  # create new DynamicArray to store old hash map
            # add old hash map to new DynamicArray
            temp.append(self._buckets[i])

        if new_capacity < 1:
            return
        # if new_capacity is prime, set new capacity to new_capacity
        if self._is_prime(new_capacity):
            self._capacity = new_capacity  # set new capacity to new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)
        self._buckets = DynamicArray()  # create new DynamicArray to store new hash map
        for i in range(self._capacity):
            # add empty LinkedLists to new hash map to be filled
            self._buckets.append(LinkedList())
        self._size = 0
        for i in range(old_capacity):
            # iterate through old hash map and add key/value pairs to new hash map
            for node in temp[i]:
                if node is not None:  # if node is not empty, add key/value pair to new hash map
                    current = node
                    while current is not None:  # iterate through LinkedList and add key/value pairs to new hash map
                        # add key/value pair to new hash map using put method
                        self.put(current.key, current.value)
                        current = current.next  # move to next node in LinkedList and return value

    def get(self, key: str):
        """
        This method (named get) returns the value associated with the given key. If the key does not exist in the hash map, the method returns None.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity  # index of bucket in hash map
        # return None if key not in hash map
        if self._buckets[index] is None:
            return None
        # iterate through LinkedList and return value if key exists
        for node in self._buckets[index]:
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        This method (named contains_key) returns True if the given key exists in the hash map, and False otherwise. An empty hash map does not contain any keys, so this method would return False.
        """
        if self._size == 0:  # if hash map is empty, return False
            return False

        # hash key to get index of bucket in hash map
        hash = self._hash_function(key)
        index = hash % self._capacity  # index of bucket in hash map

        if self._buckets[index] is None:  # if bucket is empty, return False
            return False

        # iterate through LinkedList and return True if key exists
        for node in self._buckets[index]:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        This method (named remove) removes the key/value pair from the hash map using the given key. If the key does not exist in the hash map, the method does nothing.
        """
        hash = self._hash_function(
            key)  # hash key to get index of bucket in hash map
        index = hash % self._capacity

        # iterate through LinkedList and remove key/value pair if key exists
        for node in self._buckets[index]:
            if node.key == key:
                # remove key/value pair from LinkedList
                self._buckets[index].remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method (named get_keys_and_values) returns a DynamicArray of tuples containing all the key/value pairs in the hash map. 
        The order of the tuples in the DynamicArray does not matter.
        """
        temp = DynamicArray()

        # iterate through hash map and add key/value pairs to DynamicArray
        for i in range(self._capacity):
            # if bucket is not empty, iterate through LinkedList and add key/value pairs to DynamicArray
            if self._buckets[i] is not None:
                for node in self._buckets[i]:
                    # add key/value pair to DynamicArray
                    temp.append((node.key, node.value))
        return temp

    def get_buckets(self) -> DynamicArray:
        """
        This method (named get_buckets) returns a DynamicArray of LinkedLists containing all the key/value pairs in the hash map.
        """
        return self._buckets

    def get_function(self):
        """
        This method (named get_function) returns the hash function used by the hash map.
        """
        return self._hash_function


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function (named find_mode) takes a DynamicArray of integers and returns a tuple containing a DynamicArray of the mode(s) and the number of times the mode(s) occur.
    If there is more than one value with the highest frequency, all values at that frequency should be included in the array being returned (the order does not matter). 
    If there is only one mode, the dynamic array will only contain that value.
    """
    map = HashMap()
    return_arr = DynamicArray()  # create DynamicArray to store mode(s)
    max_frequency = 1
    # iterate through DynamicArray and add key/value pairs to HashMap
    for i in range(da.length()):
        hash = map.get_function()(da[i])
        index = hash % map.get_capacity()
        if map.contains_key(da[i]):
            # get value of key in HashMap and increment by 1
            value = map.get_buckets()[index].contains(da[i]).value
            if value is not None:
                count = value + 1
                if count >= max_frequency:  # if count is greater than or equal to max_frequency, set max_frequency to count
                    max_frequency = count
                map.put(da[i], count)
        else:
            map.put(da[i], 1)  # add key/value pair to HashMap
    # iterate through HashMap and add mode(s) to DynamicArray
    for i in range(map.get_capacity()):
        # iterate through LinkedList and add mode(s) to DynamicArray
        for node in map.get_buckets()[i]:
            if node.value == max_frequency:  # if value is equal to max_frequency, add key to DynamicArray
                # add mode(s) to DynamicArray to be returned by function
                return_arr.append(node.key)
    # return tuple containing DynamicArray of mode(s) and number of times mode(s) occur
    return return_arr, max_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(),
          m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(),
          m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(),
              m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint",
            "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
