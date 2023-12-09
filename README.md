# Python_Script-CLI_Data 
##  Kajetan Jankowski

## Description
It is a recruitment task for Profil Software. It a script that performs some operations on the data.

I was trying to use principles  like SOLID, KISS or DRY.
I added SQlite3 in this project to store data in database and bcrypt to not store original passwords in DB file .
The project in open to new futures like adding new file with new extension ( already use json , xml, csv ) to add new data, or you can add new action for other role. 

## Installation 
```bash
pip install -r requirements.txt
```

## Tests
```bash
python3 test_all.py
```

## Usage
To use script.py run 

```bash
python3 script.py <command> --login <number or email> --password <password>
```
There are 6 command available:
- ## print-all-accounts (admin only) 
     Print the total number of valid accounts
```bash
python3 script.py print-all-accounts --login 817730653 --password '4^8(Oj52C+'
```

- ## print-oldest-account (admin only)
    Print information about the account with the longest existence
```bash
python3 script.py print-oldest-account --login 817730653 --password '4^8(Oj52C+'
```

- ## group-by-age (admin only)
    Group children by age
```bash
python3 script.py group-by-age --login 817730653 --password '4^8(Oj52C+'
```

- ## print-children
    Display information about the user's children
```bash
python3 script.py print-children --login 817730653 --password '4^8(Oj52C+'
```
- ## find-similar-children-by-age
    Find users with children of the same age as at least one own child
 ```bash
python3 script.py find-similar-children-by-age --login 817730653 --password '4^8(Oj52C+'
```

- ## create_database
    Remove older DB file, if exist , and create new one with data in the ./main/db/data. All files will be loaded if script supports their extensions
```bash
python3 script.py create_database
```


To get more information  use : 
```bash
python3 script.py -h 
```
## Validation
#### 1. Input Validation
- **Description:** Input validation is implemented to prevent malicious input and ensure the proper functioning of the system.
- **How it works:** login inputs is checked for correctness and then checked in DB if user is found 
- **Invalid returns**: InValid Login- User Not Found |  InValid Login- Not Valid telephone number | INValid Login- Not Valid email
#### 2. Data Integrity Checks
- **Description:** Data integrity checks are accuracy of stored data.
- **How it works:** Before data is written to the database, it undergoes integrity checks to identify and reject invalid or replace if created_at field is newer (more in ./main/db/db_manager line 78 )
#### 3. Security Validation
- **Description:** Security validation focuses on checking whether the hashed password from db is equal to the given password
- **Invalid returns**: InValid Login- Wrong password
#### 4. Role Validation
- **Description:** Role validation focuses on checking whether account has permission to use command
- **Invalid returns**: permission denied:  you are allow to use  print-children or find-similar-children-by-age














