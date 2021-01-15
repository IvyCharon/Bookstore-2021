from faker import Faker
from faker.providers import isbn
from random import randint, choice, choices, uniform, seed
import string


def unique(obj) -> list:
    ret, tmp = [], set()
    for x in obj:
        if not x in tmp:
            ret.append(x)
            tmp.add(x)
    return ret.copy()


class UserType:
    def __init__(self, user_id, passwd, authority, name):
        self.user_id = user_id
        self.passwd = passwd
        self.authority = authority
        self.name = name


class BookType:
    def __init__(self):
        self.count = 0

GeneratorSeed = 2333
TotalTestCaseNumber = 10
InstPerCase = 7500
AuthorCount = 100
MaxUserCount = 300
MaxBookCount = 1000
KeywordCount = 200
MaxStackSize = 20

seed(GeneratorSeed)
fake = Faker()
fake.seed_instance(GeneratorSeed)
fake.add_provider(isbn)

with open('../words.txt', 'r') as f:
    words = f.read().splitlines()

UserList = {'root': UserType('root', 'sjtu', 7, 'root')}
currentUser = []

AuthorList = []
for i in range(0, AuthorCount):
    AuthorList.append(''.join(fake.name().split()))

KeywordList = unique(choices(words, k = KeywordCount))

BookList = {}

def printModify(f, ISBN, name, author, keyword, price):
    if ISBN == '' and name == '' and author == '' and keyword == '' and price == '':
        return
    f.write('modify')
    if ISBN != '': f.write(' -ISBN=' + ISBN)
    if name != '': f.write(' -name="' + name + '"')
    if author != '': f.write(' -author="' + author + '"')
    if keyword != '': f.write(' -keyword="' + keyword + '"')
    if price != '': f.write(' -price=' + price)
    f.write('\n')


def Modify(BookList, Select, ISBN, name, author, keyword, price) -> str:
    if ISBN == '' and name == '' and author == '' and keyword == '' and price == '':
        return Select
    if ISBN != '':
        Book = BookList[Select]
        del BookList[Select]
        Select, Book.ISBN = ISBN, ISBN
        BookList[ISBN] = Book
    if name != '': BookList[Select].name = name
    if author != '': BookList[Select].author = author
    if keyword != '': BookList[Select].keyword = keyword
    if price != '': BookList[Select].price = price
    return Select

for i in range(1, TotalTestCaseNumber + 1):
    with open(str(i) + '.in', 'w') as f:
        currentUser = ['']
        Select = ['']
        f.write('su root ' + UserList['root'].passwd + '\n')
        currentUser.append('root')
        Select.append('')
        for j in range(1, InstPerCase + 1):
            InstType = randint(0, 8)
            if InstType <= 1 and len(BookList) != 0 and (currentUser[-1] != '' and (UserList[currentUser[-1]].authority & 2) != 0): # select old book, then modify
                #if currentUser[-1] != '': print(UserList[currentUser[-1]].authority, currentUser[-1])
                if Select[-1] == '' or randint(0, 2) == 0:
                    Select_ = Select[-1]
                    Select[-1] = choice(list(BookList.keys()))
                    f.write('select ' + Select[-1] + '\n')
                name_ = "" if randint(0, 2) == 0 else choice(words)
                author_ = "" if randint(0, 2) == 0 else choice(AuthorList)
                keyword_ = "" if randint(0, 2) == 0 else '|'.join(unique(choices(KeywordList, k = min(KeywordCount, randint(1, 5)))))
                price_ = "" if randint(0, 2) == 0 else ('%.2f' % uniform(0, 500))
                printModify(f, '', name_, author_, keyword_, price_)
                if currentUser[-1] != '' and (UserList[currentUser[-1]].authority & 2) != 0:
                    Select[-1] = Modify(BookList, Select[-1], '', name_, author_, keyword_, price_)
                else:
                    Select[-1] = Select_
            elif InstType <= 2 and len(BookList) < MaxBookCount and (currentUser[-1] != '' and (UserList[currentUser[-1]].authority & 2) != 0): # create a new book
                Select_ = Select[-1]
                Select[-1] = fake.isbn13()
                f.write('select ' + Select[-1] +'\n')
                name_ = choice(words)
                author_ = choice(AuthorList)
                keyword_ = '|'.join(unique(choices(KeywordList, k = min(KeywordCount, randint(1, 5)))))
                price_ = ('%.2f' % uniform(0, 500))
                printModify(f, '', name_, author_, keyword_, price_)
                if currentUser[-1] != '' and (UserList[currentUser[-1]].authority & 2) != 0:
                    BookList[Select[-1]] = BookType()
                    Select[-1] = Modify(BookList, Select[-1], Select[-1], name_, author_, keyword_, price_)
                else:
                    Select[-1] = Select_
            elif currentUser[-1] == '' or randint(0, 5) == 0: # su or register
                if randint(0, 20) != 0 and len(UserList) < MaxUserCount:
                    user_id = 'root'
                    while user_id in UserList.keys():
                        user_id = ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                    passwd = ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                    name = ''.join(fake.name().split())
                    f.write('register ' + user_id + ' ' + passwd + ' ' + name + '\n')
                    UserList[user_id] = UserType(user_id, passwd, 1, name)
                elif len(currentUser) < MaxStackSize:
                    currentUser.append(choice(list(UserList.keys()))), Select.append('')
                    f.write('su ' + currentUser[-1] + ' ' + UserList[currentUser[-1]].passwd + '\n')
            elif UserList[currentUser[-1]].authority == 1:
                if randint(0, 4) == 0:
                    f.write('logout' + '\n')
                    Select.pop()
                    currentUser.pop()
                else:
                    if randint(0, 8) == 0 or len(BookList) == 0: # modify passwd
                        if randint(0, 3) == 0:
                            user = choice(list(UserList.keys()))
                            old_passwd = UserList[user].passwd if randint(0, 2) == 0 else ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                        else:
                            user = currentUser[-1]
                            old_passwd = UserList[user].passwd
                        new_passwd = ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                        f.write('passwd ' + user + ' ' + old_passwd + ' ' + new_passwd + '\n')
                        if UserList[user].passwd == old_passwd: UserList[user].passwd = new_passwd
                    elif randint(0, 2) != 0: # buy books
                        ISBN_ = choice(list(BookList.keys()))
                        quantity_ = randint(0, int(BookList[ISBN_].count * 1.1)) + 1
                        f.write('buy ' + ISBN_ + ' ' + str(quantity_) + '\n')
                        if BookList[ISBN_].count >= quantity_:
                            BookList[ISBN_].count -= quantity_
                    else: # show books
                        Book = choice(list(BookList.values()))
                        f.write('show')
                        sel = randint(0, 3)
                        ISBN_ = Book.ISBN if sel == 0 else ''
                        if ISBN_ != '': f.write(' -ISBN=' + ISBN_)
                        name_ = Book.name if sel == 1 else ''
                        if name_ != '': f.write(' -name="' + name_ + '"')
                        author_ = Book.author if sel == 2 else ''
                        if author_ != '': f.write(' -author="' + author_ + '"')
                        keyword_ = choice(Book.keyword.split('|')) if sel == 3 else ''
                        if keyword_ != '': f.write(' -keyword="' + keyword_ + '"')
                        f.write('\n')
            elif randint(0, 4) == 0:
                f.write('logout' + '\n')
                Select.pop()
                currentUser.pop()
            else: # admin: useradd, import, *delete, *passwd
                t = randint(-2, 2 * (UserList[currentUser[-1]].authority >> 2) + 1)
                if (t <= 0 or t == 1 and len(BookList) == 0) and len(UserList) < MaxUserCount:
                    user_id = 'root'
                    while user_id in UserList.keys():
                        user_id = ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                    passwd = ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                    authority = UserList[currentUser[-1]].authority >> randint(1, UserList[currentUser[-1]].authority // 3)
                    name = ''.join(fake.name().split())
                    f.write('useradd ' + user_id + ' ' + passwd + ' ' + str(authority) + ' ' + name + '\n')
                    UserList[user_id] = UserType(user_id, passwd, authority, name)
                elif (t == 1 or randint(0, 1) == 0 or t == 2 and len(UserList) == 1) and len(BookList) != 0:
                    if Select[-1] == '' or randint(0, 2) == 0:
                        Select[-1] = choice(list(BookList.keys()))
                        f.write('select ' + Select[-1] + '\n')
                    quantity = randint(1, (BookList[Select[-1]].count + 10) * 2)
                    f.write('import ' + str(quantity) + ' ' + ('%.2f' % uniform(0, quantity * float(BookList[Select[-1]].price) * 1.25)) + '\n')
                    BookList[Select[-1]].count += quantity
                elif t == 2 and len(UserList) != 1:
                    user_id = 'root'
                    while user_id == 'root':
                        user_id = choice(list(UserList.keys()))
                    f.write('delete ' + user_id + '\n')
                    if not user_id in currentUser:
                        del UserList[user_id]
                elif t == 2 or t == 3: # root won't input the old-passwd
                    #print(UserList[currentUser[-1]].authority)
                    user_id = choice(list(UserList.keys()))
                    new_passwd = ''.join(choice('_' + string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(1, 30)))
                    f.write('passwd ' + user_id + ' ' + new_passwd + '\n')
                    UserList[user_id].passwd = new_passwd
                else: f.write('show finance' + ('' if randint(0, 3) == 0 else ' ' + str(randint(1, 100))) + '\n')