import mysql.connector,hashlib,uuid

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="root",
    database="rpg"
    )



def hash_password(password):
    # uuid is used to generate a random number, not implemented yet
    randomvalue = uuid.uuid4().hex
    magicnumber = str(256)
    
    return hashlib.sha256(randomvalue.encode() + password.encode()).hexdigest() + ':' + randomvalue

    
def check_password(hashed_password, user_password):
    password, randomvalue = hashed_password.split(':')
    return password == hashlib.sha256(randomvalue.encode() + user_password.encode()).hexdigest()

def insert_password() :
    new_pass = input('Please enter a password: ')
    hashed_password = hash_password(new_pass)
    old_pass = input('Now please enter the password again to check: ')
    if check_password(hashed_password, old_pass):
        return hashed_password
    else:
        print('I am sorry but the password does not match')
        insert_password()

def createUser() :
    #create new user
    user = input("Enter User Name: ")
   
    #create new hashed password (sha256) 
    hashed_password = insert_password()

    newUser= "INSERT INTO user (username,psw_hash) VALUES (%s,%s)"

    mycursor.execute(newUser,(user,hashed_password))

def createRace() :
    name = input("Enter Race name: ")
    desc = input("Race description: ")
    if desc == "" :
        desc = None
    newRace = "INSERT INTO race (race_name,race_desc) VALUES (%s,%s)"

    mycursor.execute(newRace,(name,desc))

def createClass() :
    name = input("Enter class name: ")
    desc = input("Class description: ")
    if desc == "" :
        desc = None
    newClass = "INSERT INTO class (class_name,class_desc) VALUES (%s,%s)"

    mycursor.execute(newClass,(name,desc))

def createState() :
    name = input("Enter state name: ")
    desc = input("State description: ")
    if desc == "" :
        desc = None
    newState = "INSERT INTO state (state_name,state_desc) VALUES (%s,%s)"

    mycursor.execute(newState,(name,desc))

def createAvatar() :
    name = input("Enter Your Avatar name: ")
    showAvailableClasses()
    classT = input("Select your class id: ")
    showAvailableRaces()
    raceT = input("Select your race id: ")
    
    newAvatar = "INSERT INTO avatar (name,curr_exp,max_hp,curr_hp,race,class,state) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    #hp magic number 100
    hp = 100
    startExp = 0
    defaultState = 1
    avatar = (name,startExp,hp,hp,raceT,classT,defaultState)
    mycursor.execute(newAvatar,avatar)

def showAvailableRaces() :
    selectRace = "select * from race"
    
    mycursor.execute(selectRace)
    records = mycursor.fetchall()
    print("Numer of Races: ", mycursor.rowcount)

    for row in records:
        print("Id = ", row[2], )
        print("Name = ", row[0])
        print("Desc  = ", row[1])

def showAvailableClasses() :
    selectClass = "select * from class"
    
    mycursor.execute(selectClass)
    records = mycursor.fetchall()
    print("Number of Class: ", mycursor.rowcount)

    for row in records:
        print("Id = ", row[2], )
        print("Name = ", row[0])
        print("Desc  = ", row[1])        

def showAvailableAvatars() :
    selectAvatar = "SELECT * FROM avatar"

    mycursor.execute(selectAvatar)
    records = mycursor.fetchall()
    print("Number of Created avatars: ", mycursor.rowcount)

    for row in records:
        print("Id = ", row[7])
        print("Name = ", row[0])

def showAvailableItems() :
    selectItem = "SELECT * FROM item"

    mycursor.execute(selectItem)
    records = mycursor.fetchall()
    print("Number of Created items: ", mycursor.rowcount)

    for row in records:
        print("Id = ", row[0])
        print("Name = ", row[1])

def showAvatarDetails() :
    
    showAvailableAvatars()

    selection = input("Select your avatar from its id: ")
    mycursor.execute("SELECT * FROM avatar WHERE avatar_id = ?",selection)
    avatar = mycursor.fetchall()[0]
    mycursor.execute("SELECT class_name FROM class WHERE class_id = ?",str(avatar[5]))
    classT = mycursor.fetchone()[0]
    mycursor.execute("SELECT race_name FROM race WHERE race_id = ?",str(avatar[4]))
    raceT = mycursor.fetchone()[0]
    print(avatar[0],"is a",classT,raceT,sep=" ") 

def createItem() :

    name = input("Enter item name: ")
    desc = input("Item description: ")
    if desc == "" :
        desc = None
    defaultDmg = 1
    newItem = "INSERT INTO item (item_name,item_desc,damage) VALUES (%s,%s,%s)"

    mycursor.execute(newItem,(name,desc,defaultDmg))

def createInventory() :

    showAvailableAvatars()
    avatarSel = input("Select avatar id: ")
    showAvailableItems() 
    itemSel = input("Select item id:")
    defaultQnt = 1
    newInventory = "INSERT INTO inventory (avatar_id,item_it,item_quantity) VALUES (%s,%s,%s)"
    mycursor.execute(newInventory,(avatarSel,itemSel,defaultQnt))

def showInventory() :

    showAvailableAvatars()
    avatarSel = input("Select avatar id: ")
    mycursor.execute("SELECT item,item_quantity FROM inventory WHERE avatar_id = ?",avatarSel)
    inventory = mycursor.fetchall()

    for row in inventory :
        print(row)

def createQuest() :

    name = input("Enter quest name: ")
    desc = input("Quest description: ")
    if desc == "" :
        desc = None
    defaultGiver = "Supreme Mauri"
    defaultExpGold = 1
    showAvailableItems()
    item = input("Item rewarded id: ")

    
    
    newQuest = "INSERT INTO quest (quest_giver,quest_name,gold_rwd,xp_rwd,quest_desc,item_rwd) VALUES (%s,%s,%s,%s,%s,%s)"

    mycursor.execute(newQuest,(defaultGiver,name,defaultExpGold,defaultExpGold,desc,item))

def showAvailableQuests() :
    selectQuest = "SELECT * FROM quest"

    mycursor.execute(selectQuest)
    records = mycursor.fetchall()
    print("Number of Quests: ", mycursor.rowcount)

    for row in records:
        print("Id = ", row[0])
        print("Name = ", row[3])

def createQuestJournal() : 

    showAvailableAvatars()
    avatarSel = input("Select avatar id: ")
    showAvailableQuests() 
    questSel = input("Select quest id:")
    activeQuest = 1
    newInventory = "INSERT INTO quest_journal (avatar_id,quest,state) VALUES (%s,%s,%s)"
    mycursor.execute(newInventory,(avatarSel,questSel,activeQuest))

def showQuestJournal() :

    showAvailableAvatars()
    avatarSel = input("Select avatar id: ")
    mycursor.execute("SELECT quest FROM quest_journal WHERE avatar_id = ?",avatarSel)
    journal = mycursor.fetchall()

    for row in journal :
        print(row)
def showUsers() :
    users : "SELECT username FROM user"
    mycursor.execute(users)
    records = mycursor.fetchall()

    print("Number of users: ", mycursor.rowcount)

    for row in records:
        print("Id = ", row[0], )
        print("Name = ", row[1])
        
    

def avatarList() :
    showUsers()

    selectedAccount = input("your")




mycursor = mydb.cursor(prepared=True)

createUser()

mydb.commit()
mycursor.close()
mydb.close()