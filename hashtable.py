# Initialize an empty hash table with optional initial capacity.
class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = [[] for _ in range(initial_capacity)]

    # Insert an item into the hash table.

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item  # Update value if key already exists
                return True
        bucket_list.append([key, item])
        return True

    # Lookup an item in the hash table.
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Remove an item from the hash table.
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False  # Key not found

# Example usage:
hash_table = ChainingHashTable()
hash_table.insert("package_id_1", {"delivery_address": "123 Main St", "delivery_deadline": "2024-03-10",
                                   "delivery_city": "Example City", "delivery_zip_code": "12345",
                                   "package_weight": 5.2, "delivery_status": "at the hub"})
print(hash_table.search("package_id_1"))
hash_table.remove("package_id_1")
print(hash_table.search("package_id_1"))
