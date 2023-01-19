# Name: Sean Madden
# OSU Email: maddesea@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: 12/2/2022
# Description: This program implements a hash map and utilizes open addressing. Open addressing is a method for handling hash collisions where all elements are stored in the hash table array itself
# (it has one element per bucket at most) rather than putting colliding elements in a linked list. At any given time, the hash table array may have some empty buckets (i.e., buckets that do not contain any elements).
# The hash table array is resized when the load factor (the number of elements in the hash table divided by the number of buckets) exceeds a certain threshold. The hash map is implemented using a dynamic array of
# linked lists (included in their respective classes) provided in a6_include.py.


from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        This method (named put) updates the key/value pair in the hash map. If the given key already exits in the hash map, its associated value must be replaced with the new value. 
        If the given key is not in the hash map, a new key/value pair is added to the hash map. 
        """
        if self.table_load() >= .5:  # if the table load is greater than or equal to .5
            # resize the table if the load factor is greater than or equal to .5
            self.resize_table(2 * self._capacity)  # double the capacity

        # create a new hash entry with the key and value
        element = HashEntry(key, value)  # create a new hash entry
        hash = self._hash_function(key)
        index = hash % self._capacity  # get the index
        initial_index = index  # save the initial index

        j = 1
        while self._buckets[index] is not None:  # while the bucket is not None
            if self._buckets[index].key == key:  # if the key is found
                # if the bucket is not a tombstone
                if self._buckets[index].is_tombstone is False:
                    # update the value if the key is found
                    self._buckets[index].value = value
                    return
                else:
                    self._buckets.set_at_index(index, element)
                    self._size += 1
                    return
            else:
                # quadratic probing to find the spot
                index = (initial_index + j ** 2) % self._capacity
                j += 1

        if self._buckets[index] is None:  # if the bucket is None
            # set the element at the index
            self._buckets.set_at_index(index, element)
            self._size += 1

    def table_load(self) -> float:
        """
        This method (named table_load) that returns the current load factor of the hash map.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method (named empty_buckets) that returns the number of empty buckets in the hash table.
        """
        count = 0
        for i in range(self._capacity):
            # if the bucket is None or a tombstone
            if self._buckets[i] is None or self._buckets[i].is_tombstone is True:
                count += 1  # increment the count
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        This method (named resize_table) changes the capacity of the internal hash table. Al existing key/value pairs remain in the new hash map, and all hash table links must be rehashed. 
        The method first checks if the new_capacity is not less than 1; if it is, the method does nothing but if new_capacity is 1 or greater, the method resizes the hash table to the next prime number greater than or equal to new_capacity.
        """
        # remember to rehash non-deleted entries into new table
        old_capacity = self._capacity

        # copy the old values
        temp = DynamicArray()  # create a new dynamic array
        for i in range(old_capacity):
            # copy the old values into the new array
            temp.append(self._buckets[i])

        if new_capacity < self._size:  # if new capacity is less than the size, do nothing
            return

        # check for prime
        if self._is_prime(new_capacity):
            self._capacity = new_capacity  # set new capacity
        else:
            self._capacity = self._next_prime(
                new_capacity)  # find the next prime number

        self._buckets = DynamicArray()  # reset the buckets array
        for i in range(self._capacity):  # add new buckets to the array
            self._buckets.append(None)  # add None to each bucket
        self._size = 0
        for i in range(old_capacity):
            if temp[i] is not None and temp[i].is_tombstone is False:  # not a tombstone and not None
                self.put(temp[i].key, temp[i].value)  # rehash the values

    def get(self, key: str) -> object:
        """
        This method (named get) returns the value associated with the given key. If the key does not exist in the hash map, the method returns None.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        initial_index = index  # save the initial index
        j = 1
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:  # found the key in the table
                if self._buckets[index].is_tombstone:  # if it is a tombstone
                    return None
                else:
                    # return value if key is found
                    return self._buckets[index].value
            else:
                # quadratic probing to find the spot
                index = (initial_index + j ** 2) % self._capacity
                j += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method (named contains_key) returns True if the given key exists in the hash map, and False otherwise. An empty hash map does not contain any keys, so this method would return False.
        """
        if self._size == 0:
            return False  # empty hash map does not contain any keys
        # ternary operator to return True or False
        return True if self.get(key) is not None else False

    def remove(self, key: str) -> None:
        """
        This method (named remove) removes the key/value pair from the hash map using the given key. If the key does not exist in the hash map, the method does nothing.
        """
        hash = self._hash_function(key)  # hash the key to get the index
        index = hash % self._capacity  # get the index
        initial_index = index  # save the initial index for quadratic probing

        if self.contains_key(key):  # if the key is in the hash map
            j = 1
            # find the key in the table and set it to a tombstone
            while self._buckets[index].key != key:
                # quadratic probing to find the spot to remove
                index = (initial_index + j ** 2) % self._capacity
                j += 1
            self._buckets[index].is_tombstone = True  # set tombstone to true
            self._size -= 1

    def clear(self) -> None:
        """
        This method (named clear) removes all key/value pairs from the hash map. IT does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        i = 0
        while i < self._capacity:  # make sure to set all elements to None
            self._buckets.append(None)
            i += 1
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method (named get_keys_and_values) returns a DynamicArray of tuples containing all the key/value pairs in the hash map. 
        The order of the tuples in the DynamicArray does not matter.
        """
        temp = DynamicArray()  # temp array to hold the key/value pairs
        for i in range(self._capacity):  # loop through the buckets
            # if the bucket is not None and not a tombstone append the key/value pair to the temp array
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                temp.append((self._buckets[i].key, self._buckets[i].value))
        return temp  # return the temp array

    def __iter__(self):
        """
        This method (named __iter__) returns an iterator for the hash map. The iterator returns the keys in the hash map in an arbitrary order.
        """
        if not self._size:  # if the size is 0
            for key, value in self.get_keys_and_values():  # loop through the key/value pairs
                yield key, value

    def __next__(self):
        """
        This method (named __next__) returns the next key in the hash map, based on the current location of the iterator.
        """
        return self.__iter__()  # return the iterator


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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
