# keys are string/value pair
# only one transaction can exist at a time
# within a transaction can make as many changes as you want but not visible to get until committed 
# transaction ends when commit or rollback is called


class TransactionError(Exception):
    pass

class KeyValueDatabase:
    def __init__(self):
        self._main_db = {}
        self._transaction_db = {}
        self._in_transaction = False

    def begin_transaction(self):
        # starts a new transaction
        if self._in_transaction:
            raise TransactionError("Transaction already in progress")
        self._in_transaction = True
        self._transaction_db.clear()

    def put(self, key, value):
        # create a new key with provided value if key doesn't exist
        # otherwise update existing key
        # if put called when transaction not in progress throw an exception
        if not self._in_transaction:
            raise TransactionError("No transaction in progress")
        self._transaction_db[key] = value

    def get(self, key):
        # return the value associated with the key or null if the key doesn't exist
        # get key can be called any time even when a transaction is not in progress
        if self._in_transaction and key in self._transaction_db:
            return self._transaction_db[key]
        return self._main_db.get(key)

    def commit(self):
        # applied to changes made within the transaction to the main state
        # allows any future gets to see the changes made in the transaction
        if not self._in_transaction:
            raise TransactionError("No transaction in progress")
        self._main_db.update(self._transaction_db)
        self._end_transaction()

    def rollback(self):
        # should abort all changes made within the transaction and everything 
        # should go back to the way it was before
        if self._in_transaction:
            print("Transaction rolled back.")
            self._end_transaction()
        else:
            print("No transaction to roll back.")

    def _end_transaction(self):
        """Helper method to clear transaction data and state."""
        self._transaction_db.clear()
        self._in_transaction = False

def main():
    db = KeyValueDatabase()
    actions = {
        'BEGIN': db.begin_transaction,
        'PUT': lambda: db.put(input("Enter key: ").strip(), int(input("Enter integer value: "))),
        'GET': lambda: print(f"The value at key '{key}' is {db.get(key)}" if (key := input("Enter key: ").strip()) in db._main_db or db._in_transaction else "No value found for key."),
        'COMMIT': db.commit,
        'ROLLBACK': db.rollback,
        'EXIT': exit
    }

    while True:
        action = input("\nOptions: BEGIN, PUT, GET, COMMIT, ROLLBACK, EXIT\nChoose an action: ").strip().upper()
        try:
            actions.get(action, lambda: print("Invalid action. Please choose a valid option."))()
        except TransactionError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
