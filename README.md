<h1 align="center">Accountant bot</h1>

<p align="center">


<img src="https://img.shields.io/badge/python-3.5.7-yellow.svg">

<img src="https://img.shields.io/badge/pyTelegramBotAPI-4.3.1-blue.svg">

<img src="https://img.shields.io/badge/XlsxWriter-3.0.3-green.svg">

<img src="https://img.shields.io/badge/sqlite3-2.5-white.svg">

</p>
Accountant bot for the "Telegram" messenger 

---
Accountant bot in which you can add your revenues and expenses. Bot gives statistics for a certain period and also the history of records in excel file.

Sqlite data connected to the bot. It consists of 3 tables: users, categories, revenues_and_expenses

Made with the pyTelegramBotAPI in Python language


<p align="center">
<img src="https://media.giphy.com/media/YCbfZ3aEm0EBvTluVP/giphy.gif">
</p>

# Installation and launching

```
# make sure that you are in the project folder
pip install requirements.txt 
python3 main.py 
```


### All functions

- **start/help** - adding a user to the database and creates basic categories
- **delete** - deleting all information about the user
- **categories** - viewing available categories
- **statistics_(period)** - viewing statistics for a certain period
- **excel** - sending an excel file with the history of all records
- **+(amount) (category)** - adding revenue 
- **-(amount) (category)** - adding expense

### Several challenges

| Problem                                                                                                                      | Solution                                                                                                                      |
|------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| The large number of database calls makes the code in main.py difficult to read                                               | I put all the database logic in a separate file. it consists of an accountant class with the necessary functions              | 
| The datetime library will not allow you to subtract months from a certain date only days (not all months consist of 30 days) | Use the dateutil library, which can be used to subtract months and years                                                      |
| A person can add a lot of records per day, so you need to make it as easy as possible                                        | At the beginning of bot use, show a simple way to add a record (+amount/-amount category) and check the text sent by the user |


### Some more gifs
<p align="center">
<img src="https://media.giphy.com/media/ajjQEwPjmX7CrDADLJ/giphy.gif">
</p>
<p align="center">
<img src="https://media.giphy.com/media/t5K0LG0dsy1lGNlLHj/giphy.gif">
</p>
<p align="center">
<img src="https://media.giphy.com/media/ySkAQyoNnxNTPWX2zL/giphy.gif">
</p>
<p align="center">
<img src="https://media.giphy.com/media/8YTTnxO4rkStxcyLU1/giphy.gif">
</p>
<p align="center">
<img src="https://media.giphy.com/media/7GhGk58dRSHoZtzUqI/giphy.gif">
</p>