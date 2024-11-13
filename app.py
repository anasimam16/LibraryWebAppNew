from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)    #to initialise flask, imptt whenever creating flask
app.secret_key = "secretkey"   #create scretkey to protect from malpratice

#Initialize the SQLite database
def init_sqlite_db():     #initialise database
    conn = sqlite3.connect("library.db")  #connecting to library database
    conn.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)")
    conn.close()

init_sqlite_db()


# Home Page - Display All Books
#Function for displayin homepage i.e. all books will be displayed on homepage
@app.route('/')
#route is used to redirect the page
def index():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template("index.html", books=books)  #render means open, it will display all the list of books in index.html

#Add a New Book  #Insert a new row
@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        if title and author and year:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
            conn.commit()   #saving changes
            conn.close()
            flash("Book added successfully!")    # flash used to print any message on webpage
            return redirect(url_for('index'))    #redirect to home page i.e. index.html
        else:
            flash("All fields are required!")
    return render_template('add_book.html')


#Update book function will be triggered based on id
#Update a Book - take id of book and call /update_book url and edit
@app.route('/update_book/<int:id>', methods=["GET", "POST"])
def update_book(id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()      #when selecting we are using get which we will redirect to update url
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()
    conn.close()

    if request.method == "POST":    #when submitting detail we are using post
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        if title and author and year:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, id))
            conn.commit()    
            conn.close()
            flash("Book updated successfully!")      
            return redirect(url_for('index'))     
        else:
            flash("All fields are required!")
    
    return render_template('update_book.html', book=book)

#Delete a Book - take id of book and delete_book url and delete
@app.route('/delete_book/<int:id>', methods=["GET"])  #GET is used when submission is taken with the url
def delete_book(id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Book deleted successfully!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)   #it ensures flask funcn runs only when this while exists and executed by flask server
    #app.run will start flask server and we can see webpage
    #debug allows app to reload and also shows error if there is one





