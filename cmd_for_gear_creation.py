from game_lib import *
from server import *
import base64


'''item = Purify("physical", 5, 7, 0)'''
'''with open("C:/Users/Gekoga/Downloads/1200px-Wiktor_Michajlowitsch_Wassnezow_003.jpg", "rb") as file:
    file = file.read()

    encoded = base64.encodebytes(file)
    sqlite_update("""INSERT INTO Image(Pickle)
                    VALUES(?)""", (encoded,))

with open("output.jpg", "wb") as file2:
    encoded = sqlite_request("""SELECT Pickle FROM Image
                                WHERE ImageId = ?""", (2,))[0][0]
    encoded = base64.decodebytes(encoded)
    file2.write(encoded)
    file2.close()'''

index = sqlite_request("""SELECT Pickle FROM Image
                            WHERE ImageId = ?""", (2,))[0][0]

sqlite_update("""""", (index, 904222744))

'''item = pickle.loads(item)
item.rarity = "epic"
sqlite_update("""UPDATE Ability
                SET Pickle = ?
                WHERE Name = ?""", (pickle.dumps(item), str(item)))'''
