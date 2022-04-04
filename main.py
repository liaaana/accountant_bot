import os
import telebot
import datetime
from dateutil.relativedelta import relativedelta
from config import BOT_TOKEN, BASIC_CATEGORIES
from db_functions import Accountant
from xlsxwriter.workbook import Workbook

bot = telebot.TeleBot(BOT_TOKEN)
bot_db = Accountant('db/accountant.db')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if bot_db.does_user_exist(message.chat.id) is None:
        bot_db.add_user(message.chat.id)
        for category in BASIC_CATEGORIES:
            bot_db.add_category(message.chat.id, category)
    bot.send_message(message.chat.id, 'Hi! I\'m a bot for recording income and expenses.\nEnter:\n/start or /help '
                                      '- to find out what I\'m good at.\n/delete - to remove your data from the '
                                      'database.\n/categories - to find out the available categories.\n/exel - to get '
                                      'the data in excel file format\n/statistics - to find out the statistics\n +('
                                      'amount) (category name) - to add income. For example: +500 salary\n -(amount) ('
                                      'category name) - to add an expense. For example: -200 food')


@bot.message_handler(commands=['delete'])
def delete(message):
    if bot_db.does_user_exist(message.chat.id) is not None:
        bot_db.delete_categories(message.chat.id)
        bot_db.delete_all_revenues_and_expenses(message.chat.id)
        bot_db.delete_user(message.chat.id)
        bot.send_message(message.chat.id, 'Deleted.Goodbye!')
    else:
        bot.send_message(message.chat.id, "You aren't in in database")


@bot.message_handler(commands=['categories'])
def categories(message):
    if bot_db.does_user_exist(message.chat.id) is not None:
        res = ''
        users_categories = bot_db.get_categories_by_user_id(message.chat.id)
        for i in users_categories:
            res += f'{list(i)[2]}' + '\n'
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, "You aren't in in database. Press /start to use")


@bot.message_handler(commands=['statistics'])
def help_statistics(message):
    bot.send_message(message.chat.id, "To get the statistics for:\nprevious day - /statistics_previous_day\n"
                                      "current day - /statistics_current_day\nprevious month - "
                                      "/statistics_previous_month\ncurrent month - "
                                      "/statistics_current_month\nprevious year - /statistics_previous_year\ncurrent "
                                      "year - /statistics_current_year\nall time - /statistics_all_time")


@bot.message_handler(commands=['statistics_previous_day', 'statistics_current_day', 'statistics_previous_month',
                               'statistics_current_month', 'statistics_previous_year', 'statistics_current_year',
                               'statistics_all_time'])
def statistics(message):
    if bot_db.does_user_exist(message.chat.id) is not None:
        records = bot_db.get_revenues_and_expenses_by_user_id(message.chat.id)
        dt_now = datetime.datetime.now()
        users_categories = bot_db.get_categories_by_user_id(message.chat.id)
        revenues = [0 for _ in range(len(users_categories))]
        expenses = [0 for _ in range(len(users_categories))]
        first_category_id = list(users_categories[0])[0]
        if records is not None:
            if 'statistics_previous_day' in message.text:
                records = [i for i in records if datetime.datetime.strptime(list(i)[5], '%Y-%m-%d %H:%M:%S').day == (
                            dt_now - relativedelta(days=1)).day]
            elif 'statistics_current_day' in message.text:
                records = [i for i in records if
                           datetime.datetime.strptime(list(i)[5], '%Y-%m-%d %H:%M:%S').day == dt_now.day]
            elif 'statistics_previous_month' in message.text:
                records = [i for i in records if datetime.datetime.strptime(list(i)[5], '%Y-%m-%d %H:%M:%S').month == (
                            dt_now - relativedelta(months=1)).month]
            elif 'statistics_current_month' in message.text:
                records = [i for i in records if
                           datetime.datetime.strptime(list(i)[5], '%Y-%m-%d %H:%M:%S').month == dt_now.month]
            elif 'statistics_previous_year' in message.text:
                records = [i for i in records if datetime.datetime.strptime(list(i)[5], '%Y-%m-%d %H:%M:%S').year == (
                            dt_now - relativedelta(years=1)).year]
            elif 'statistics_current_year' in message.text:
                records = [i for i in records if
                           datetime.datetime.strptime(list(i)[5], '%Y-%m-%d %H:%M:%S').year == dt_now.year]
            balance = 0
            records.sort(key=lambda x: x[2])
            for i in records:
                record_id, user_id, category_id, operation_type, amount, date = i
                if operation_type == 1:
                    balance += amount
                    revenues[category_id - first_category_id] += amount
                else:
                    balance -= amount
                    expenses[category_id - first_category_id] += amount
            res = ''
            for i in range(len(users_categories)):
                if revenues[i] - expenses[i] != 0:
                    if revenues[i] - expenses[i] > 0:
                        res += f'{list(users_categories[i])[2]}: +{revenues[i] - expenses[i]}\n'
                    else:
                        res += f'{list(users_categories[i])[2]}: {revenues[i] - expenses[i]}\n'
            if sum(expenses) != 0:
                expenses = [-i for i in expenses]
            bot.send_message(message.chat.id,
                             f'Revenues: {sum(revenues)}\nExpenses: {sum(expenses)}\nBalance: {balance}\n'
                             f'By categories:\n{res}')
        else:
            bot.send_message(message.chat.id, "You haven't got any records")
    else:
        bot.send_message(message.chat.id, "You aren't in in database. Press /start to use")


@bot.message_handler(commands=["excel"])
def exel(message):
    if bot_db.does_user_exist(message.chat.id) is not None:
        workbook = Workbook(f'files/{str(message.chat.id)}' + '.xlsx')
        worksheet = workbook.add_worksheet()
        data = bot_db.get_revenues_and_expenses_by_user_id(message.chat.id)
        data_upd = []
        for i in data:
            record_id, user_id, category_id, operation_type, amount, date = i
            amount = amount if operation_type else amount * -1
            data_upd.append([bot_db.get_category_by_id(category_id)[0], amount, date])
        for i in range(len(data_upd)):
            for j in range(len(data_upd[i])):
                worksheet.write(i, j, data_upd[i][j])
        workbook.close()
        f = open(f'files/{str(message.chat.id)}' + '.xlsx', "rb")
        bot.send_document(message.chat.id, f)
        os.remove(f'files/{str(message.chat.id)}' + '.xlsx')
    else:
        bot.send_message(message.chat.id, "You aren't in database. Press /start to use")


@bot.message_handler(content_types=["text"])
def income_or_expense(message):
    if bot_db.does_user_exist(message.chat.id) is not None:
        operation_type = None
        if message.text.startswith('-'):
            operation_type = 0
        elif message.text.startswith('+'):
            operation_type = 1
        if operation_type is not None:
            info = message.text[1:].split()

            value_is_correct = 1
            for i in info[0]:
                if not (i.isdigit() or i == '.' or i == ','):
                    value_is_correct = 0
                    break
            if value_is_correct:
                amount = float(info[0].replace(',', '.'))
                if len(info) == 2:
                    users_categories = bot_db.get_categories_by_user_id(message.chat.id)
                    for i in users_categories:
                        category_name = list(i)[2]
                        if category_name == 'other':
                            bot_db.add_revenue_or_expense(message.chat.id, list(i)[0], operation_type, amount)
                            break
                        if info[1] in category_name:
                            bot_db.add_revenue_or_expense(message.chat.id, list(i)[0], operation_type, amount)
                            break
                    if operation_type == 0:
                        bot.send_message(message.chat.id, "Your expense added to the database.")
                    else:
                        bot.send_message(message.chat.id, "Your income added to the database.")
                else:
                    bot.send_message(message.chat.id, "Category is not defined")
            else:
                bot.send_message(message.chat.id, "The amount is incorrect")
        else:
            bot.send_message(message.chat.id,
                             "You didn't specify the type of operation ('+' or '-' at the beginning of the message)")
    else:
        bot.send_message(message.chat.id, "You aren't in in database. Press /start to use")


if __name__ == '__main__':
    bot.infinity_polling()
