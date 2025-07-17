# Library_Management_System
A basic library management system made using Python and MySQL.

It is supposed to be used by the library management staff.

This library management system uses 2 tables in MySQL to work, namely 'books' and 'issue'.

Table 'books' keeps the records of every single book currently owned by the library. It even has those books in its records which are not currently physically available in the library as they have been issued.

Table 'issue' keeps the records of all the issued books and who have they been issued to.

Schema of 'books':-

  There are 4 columns. They are in the correct order as follows:-

    Bcode: This is a primary key and its type is varchar(10). It is short for 'Book code' and is used to uniquely identify every single book in the library even among multiple copies of the same book.

    Bname: Its type is varchar(50). It is short for 'Book name'.

    Author: Its type is varchar(50).

    Subject: Its type is varchar(50).

Schema of 'issue':-

  There are 4 columns. They are in the correct order as follows:-

    Student_name: Its type is varchar(50).

    Unique_Student_Identifier: Its type is varchar(10)

    Bcode: Its type is varchar(10). It is a foreign key and is associated to the 'Bcode' column in table 'books'.

    Issue_date: Its type is date.
