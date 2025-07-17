import mysql.connector
from datetime import date
connection=mysql.connector.connect(host='localhost',user='root',password='your_MySQL_password',database='your_database_name')
mycursor=connection.cursor(buffered=True)
def addbooks():
    num=int(input('Enter number of books to be added: '))
    lst=[]
    print('\n')
    b_codes=[]
    for x in range(num):
        book_code=input('Enter book code: ')
        title=input('Enter book title: ')
        author=input('Enter author name: ')
        subject=input('Enter subject(book type): ')
        mycursor.execute('select bcode from books where bcode=%s',(book_code,))
        if (book_code in b_codes) or (mycursor.fetchone() is not None):
            print('\nThis book code is either already assigned to another book in library or has been previously mentioned by you')
            continue
        b_codes.append(book_code)
        lst.append((book_code,title,author,subject))
        print('\n')
    if lst:
        mycursor.executemany('insert into books values(%s,%s,%s,%s)',lst)
        connection.commit()
        print('\nAll book(s) that could be added have been added successfully\n')
        print('\n----------------------------------------------------------------------------------------')
        return
    print('\nNo new books have been added')
    print('\n----------------------------------------------------------------------------------------')
def issue():
    mycursor.execute('select * from books')
    if not mycursor.fetchone():
        print('No books are available for issue yet')
        return
    num=int(input('Enter number of books to be issued: '))
    lst=[]
    print('\n')
    b_codes=[]
    name=input('Enter your name: ')
    unique_identifier=input('Enter your unique_identifier: ')
    for x in range(num):
        book_code=input('Enter book code: ')
        mycursor.execute('select bcode from issue where bcode=%s',(book_code,))
        if mycursor.fetchone() is not None:
            print('\nThis book is currently issued')
            continue
        mycursor.execute('select bcode from books where bcode=%s',(book_code,))
        if (book_code in b_codes) or (mycursor.fetchone() is None):
            print('\nThis book either does not exist in library or has been previously mentioned by you')
            continue
        b_codes.append(book_code)
        lst.append((name,unique_identifier,book_code,str(date.today())))
        print('\n')
    if lst:
        mycursor.executemany('insert into issue values(%s,%s,%s,%s)',lst)
        connection.commit()
        print('\nAll book(s) that could be issued have been issued successfully\n')
        print('\n----------------------------------------------------------------------------------------')
        return
    print('No new books have been issued')
    print('\n----------------------------------------------------------------------------------------')
def submit():
    mycursor.execute('select * from issue')
    if mycursor.fetchone() is None:
        print('No books have been issued yet')
        print('\n----------------------------------------------------------------------------------------')
        return
    num=int(input('Enter number of books to be submitted: '))
    lst=[]
    for x in range(num):
        book_code=input('Enter book code: ')
        mycursor.execute('select bcode from issue where bcode=%s',(book_code,))
        if ((book_code,) in lst) or (mycursor.fetchone() is None):
            print('This book is either not issued or has been previously mentioned by you')
            continue
        lst.append((book_code,))
        print('\n')
    if lst:
        mycursor.executemany('delete from issue where bcode=%s',lst)
        connection.commit()
        print('\nAll book(s) that can be submitted have been submitted successfully\n')
        print('\n----------------------------------------------------------------------------------------')
        return
    print('No book(s) that can be submitted have been inputted')
    print('\n----------------------------------------------------------------------------------------')
def removebooks():
    num=int(input('Enter number of books to be removed: '))
    lst=[]
    for x in range(num):
        book_code=input('Enter book code: ')
        mycursor.execute('select bcode from books where bcode=%s',(book_code,))
        if ((book_code,) in lst) or (mycursor.fetchone() is None):
            print('\nThis book either does not exist in library or has been previously mentioned by you\n')
            continue
        mycursor.execute('select bcode from issue where bcode=%s',(book_code,))
        if mycursor.fetchone() is not None:
            print('\nThis book is currently issued\n')
            continue
        lst.append((book_code,))
        print('\n')
    if lst:
        mycursor.executemany('delete from books where bcode=%s',lst)
        connection.commit()
        print('\nAll book(s) that can be removed have been removed successfully\n')
        print('\n----------------------------------------------------------------------------------------')
        return
    print('No book(s) have been removed')
    print('\n----------------------------------------------------------------------------------------')
def displayallbooks():
    mycursor.execute('select * from books')
    allbooks=mycursor.fetchall()
    if not allbooks:
        print('The library currently has no books\n')
        return
    for x in allbooks:
        print(f'Book Code: {x[0]}')
        print(f'Book Name: {x[1]}')
        print(f'Book Author: {x[2]}')
        print(f'Book Subject: {x[3]}')
        print('\n')
    print('\n----------------------------------------------------------------------------------------')
def displayissuedbooks():
    mycursor.execute('select * from issue')
    issuedbooks=mycursor.fetchall()
    if not issuedbooks:
        print('No books have been issued right now\n')
        print('\n----------------------------------------------------------------------------------------')
        return
    for x in issuedbooks:
        print(f'Book Code: {x[2]}')
        print(f'Student unique_identifier: {x[1]}')
        print(f'Student Name: {x[0]}')
        print(f'Issue date: {x[3]}')
        print('\n')
    print('\n----------------------------------------------------------------------------------------')
def dispavailbooks():
    mycursor.execute('select * from books where bcode not in (select bcode from issue)')   #Minus operation between books and issue
    availbooks=mycursor.fetchall()
    if not availbooks:
        print('No books are available for issue right now\n')
        return
    for x in availbooks:
        print(f'Book Code: {x[0]}')
        print(f'Book Name: {x[1]}')
        print(f'Book Author: {x[2]}')
        print(f'Book Subject: {x[3]}')
        print('\n')
    print('\n----------------------------------------------------------------------------------------')
def main():
    print('Please select an option\nYour choices are:-')
    while True:
        print('\nOption 1 -> Add a book in library database')
        print('Option 2 -> Delete a book from library database')
        print('Option 3 -> Issue a book')
        print('Option 4 -> Submit a book')
        print('Option 5 -> Display all library books')
        print('Option 6 -> Display all issued book')
        print('Option 7 -> Display all books available for issue')
        print('Option 8 -> Exit')
        choice=input('\nEnter your option: ')
        match choice:
            case '1':addbooks()
            case '2':removebooks()
            case '3':issue()
            case '4':submit()
            case '5':displayallbooks()
            case '6':displayissuedbooks()
            case '7':dispavailbooks()
            case '8':break
            case _:print('Invalid option\nTry again')
print('\nEnter password but you will only be given three chances\n')
for x in range(3):
    pwd=input('Enter password: ')
    if pwd=='abcd':
        main()
        break
    else:
        print('Incorrect password')
print('\nGoodbye')
mycursor.close()
connection.close()