import sqlite3

class GroceryList:
    next_id = 1

    def __init__(self, owner, items=None):
        self.items = items if items is not None else []
        self.id = GroceryList.generate_id()
        self.owner = owner
        self.collaborators = []

    @classmethod
    def generate_id(cls):
        current_id = cls.next_id
        cls.next_id += 1
        return current_id

    def addItems(self, objects):
        list_objects = objects.split(",")
        for i in list_objects:
            if i.lower().strip() in self.items:
                continue
            self.items.append(i.lower().strip())
        return "Successful addition of items to your list!"

    def remove_items(self, objects):
        errors = 0
        list_objects = objects.split(",")
        if not self.items:
            return "Your shopping list is empty!"
        for i in list_objects:
            if i.lower().strip() not in self.items:
                errors += 1
            else:
                self.items.remove(i)
        print(f"Successfully removed items. {errors} items you mentioned are not in your list!")

    def add_collaborator(self, user):
        if not self.collaborators:
            self.collaborators.append(user)
        else:
            print("This grocery list already has a collaborator.")

    def save_to_db(self):
        connections = sqlite3.connect("clients.db")
        cursor = connections.cursor()
        cursor.execute("INSERT INTO lists (full_name, tasks_lists, collaborating, collaborated) VALUES (?, ?, ?, ?)",
                       (self.owner.full_name, ','.join(self.items), self.collaborators[0] if self.collaborators else '', 0))
        connections.commit()
        connections.close()

    def __str__(self):
        return f'Grocery List for {self.owner.full_name}: {self.items}'
