from server import *
import base64


item = Weapon("Poisoned knife", "rare", 4, "range", attack_effect=(Poisoned, 2, 2, 1, 1.5))
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
    file2.close() 192.168.1.207

index = sqlite_request("""SELECT Pickle FROM Image
                            WHERE ImageId = ?""", (2,))[0][0]

sqlite_update("""""", (index, 904222744))'''

sqlite_update("""UPDATE Weapon
                SET Pickle = ?
                Where WeaponId = ?""", (pickle.dumps(item), 1))
