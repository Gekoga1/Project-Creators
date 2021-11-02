from game_lib import *
from server import *


item = Armor("Vanguard Shoulders", "uncommon", [2, 1, 0, 1, 0, 0, 0, 0], 8, 2)
sqlite_update("""INSERT INTO Armor(Pickle, Name, Rarity)
                VALUES(?, ?, ?)""", (pickle.dumps(item, 3), item.name, item.rarity))

'''item = sqlite_request("""SELECT Pickle FROM Armor
                        WHERE Name = ?""", ("Leather suit",))[0][0]

item = pickle.loads(item)
item.rarity = "epic"
sqlite_update("""UPDATE Armor
                SET Pickle = ?
                WHERE Name = ?""", (pickle.dumps(item), "Leather suit"))'''
