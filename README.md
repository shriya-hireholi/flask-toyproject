# ToDo Flask Project 

## To run this project

Clone this repo

Move to the folder  flask-toyproject-shriya

Create a virtual environment and activate it.

Install all dependencies

```bash
pip3 install -r requirements.txt
```

<hr>

### To create databse and tables

In *toyproject* folder under **__init__.py** file, put down the username and password of your postgres.

Then run the following commands:

```bash  
$ python
$ from toyproject import db
$ db.create_all()
$ exit()
```
<hr>

### Now that the Database is set,

Run the following command:
```bash
python3 run.py
```

<hr>

### To delete the Database

```bash  
python3 drop_db.py 
```
