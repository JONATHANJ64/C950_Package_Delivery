class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = [[] for _ in range(initial_capacity)]

    def insert(self, key, item):
        # Insert an item into the hash table.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        bucket_list.append([key, item])
        return True

    def search(self, key):
        # Lookup an item in the hash table.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        # Remove an item from the hash table.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for i, kv in enumerate(bucket_list):
            if kv[0] == key:
                del bucket_list[i]  # Remove the key-value pair
                return True
        return False  # Key not found

# Example usage:
# hash_table = ChainingHashTable()

# hash_table.insert("package_id_1", {"delivery_address": "123 Main St", "delivery_deadline": "2024-03-10",
#  "delivery_city": "Example City", "delivery_zip_code": "12345",
# "package_weight": 5.2, "delivery_status": "at the hub"})

# print(hash_table.search("package_id_1"))
# hash_table.remove("package_id_1")
# print(hash_table.search("package_id_1"))
