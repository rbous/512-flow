import time

class GroceryList:
    id = 0
    def __init__(self, owner, items = None):
        self.items = items if items is not None else []
        self.id = GroceryList.generate_id()
        self.owner = owner
        GroceryList.id += 1
        self.collaborators = []

    @classmethod
    def generate_id(cls):
        cls.id += 1
        return cls.id

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
        if objects is None:
            return "Your Shopping list is empty!"
        else:
            for i in list_objects:
                if i.lower().strip() not in self.items:
                    errors += 1
                else:
                    self.items.remove(i)
            print(f"Successfully removed Items. {errors} items you have mentionned are not in your list!")
 
        

    def add_collaborator(self, user):
        if not self.collaborators: 
            self.collaborators.append(user)
        else:
            print("This grocery list already has a collaborator.")
        
        


