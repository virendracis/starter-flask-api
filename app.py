from flask import Flask, render_template, request, redirect
from datetime import datetime

# create the app
app = Flask(__name__)


class SimpleDatabase:
    def __init__(self):
        self.items = []

    def insert_item(self, title, desc):
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_item = {
            'sno': len(self.items) + 1,
            'title': title,
            'desc': desc,
            'date_created': date_created
        }
        self.items.append(new_item)
        print("Item inserted successfully.")

    def get_all_items(self):
        return self.items

    def get_item_by_id(self, item_id):
        for item in self.items:
            if item['sno'] == item_id:
                return item
        return None

    def update_item(self, item_id, title, desc):
        for item in self.items:
            if item['sno'] == item_id:
                item['title'] = title
                item['desc'] = desc
                item['date_created'] = datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')
                print("Item updated successfully.")
                return
        print("Item not found.")

    def delete_item(self, item_id):
        for index, item in enumerate(self.items):
            if item['sno'] == item_id:
                del self.items[index]
                print("Item deleted successfully.")
                return
        print("Item not found.")


db = SimpleDatabase()


def calculation(s):
    arr = s.strip().split("\t")
    mins = 0

    for item in arr:
        if 'hrs' in item:
            hours = int(item.split(' ')[0])
            minutes = int(item.split(' ')[2])

            if hours > 8:
                mins += (hours - 8) * 60 + minutes
            elif hours < 8:
                mins -= (7 - hours) * 60 + (60 - minutes)
            else:
                mins += minutes

    return {'mins': f'{mins} Minutes', 'hrs': f'{mins//60} Hours, {mins%60} Minutes'}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # Create
        db.insert_item(title, desc)
    # Read
    allTodo = db.get_all_items()
    return render_template('index.html', allTodo=allTodo)


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    hours = 0
    if request.method == 'POST':
        hours = request.form['hours']
        hours = calculation(hours)
    allTodo = db.get_all_items()
    return render_template('index.html', hours=hours, allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # Update
        db.update_item(sno, title, desc)
        return redirect("/")

    todo = db.get_item_by_id(sno)
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    # Delete
    db.delete_item(sno)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
