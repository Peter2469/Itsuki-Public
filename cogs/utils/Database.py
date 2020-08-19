import sqlite3

from sqlite3 import Error


class Database():
    # Class Fields
    db = None

    # Constructors
    def __init__(self):
        self.db = None
        

    # Generic Database Methods
    """
    Connects to the database file specified

    param dbFile:    Name of the Database File e.g "test.db"
    return: None
    """
    def connect(self, dbFile):
        if self.db is None:
            try:
                self.db = sqlite3.connect(dbFile)
            except Error as e:
                print(e)

    """
    Closes the database that is currently connected to

    param: None
    return: None
    """
    def close(self):
        if self.db is not None:
            self.db.close()
        else:
            print("Error: Cannot close a database since no database has been opened")

    """
    Creates a table with given SQL query
    param sqlQuery: An SQL query to create a table
    return: None
    """
    def createTable(self, sqlQuery):
        if self.db is not None:
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery)
            except Error as e:
                print(e)
        else:
            print("Error: Cannot create a table when no database exists")

    """
    Drops a table with the given SQL query

    param sqlQuery: An SQL query to drop a specified table
    return: None
    """
    def dropTable(self, sqlQuery):
        if self.db is not None:
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery)
            except Error as e:
                print(e)
        else:
            print("Error: Cannot drop a table when no database exists")

    """
    Displays a table with the given SQL query

    param sqlQuery: An SQL query to select information from an existing table
    return: None
    """
    def displayTable(self, sqlQuery):
        if self.db is not None:
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery)
                tableContent = cursor.fetchall()
                for content in tableContent:
                    print(content, "\n")
            except Error as e:
                print(e)
        else:
            print("Error: Cannot display a table when no database exists")

    """
    Commits any changes made to the database in memory to the database file.
    Essentially saves your changes made to the database since you connected to it.

    param: None
    return: None
    """
    def commit(self):
        if self.db is not None:
            try:
                self.db.commit()
            except Error as e:
                print(e)
        else:
            print("Error: Cannot commit changes when no database exists")


    # Implementation Specific Database Methods
    """
    You will need to create your own methods here depending on what tables you create in your database.
        
    Use these methods as a guideline for creating your own
    These methods are assuming that there are two tables, a project table, and a task table.
    Check the Main.py file for the specifics on the table's attributes.
    """

    """
    Creates a new project in the projects table.
    This is an example so the method you would create would be specific to the type of table
    you have created in your database.

    param project: A list of arguments defining a new project
    return: Returns the Row ID of where the new project was inserted into the projects table
    """
    def createProject(self, project):
        projRowId = -1
        if self.db is not None:
            sqlQuery = ''' INSERT INTO projects(name, begin_date, end_date)
                           VALUES(?,?,?) '''
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery, project)
                projRowId = cursor.lastrowid
            except Error as e:
                print(e)
        else:
            print("Error: Cannot create project when no database exists")
            
        return projRowId

    """
    Creates a new task in the tasks table.
    This is an example so the method you would create would be specific to the type of table
    you have created in your database.

    param task: A list of arguments defining a new task
    return: Returns the Row ID of where the new task was inserted into the tasks table
    """
    def createTask(self, task):
        taskRowId = -1
        if self.db is not None:
            sqlQuery = '''INSERT INTO tasks(name, priority, status_id, project_id, begin_date, end_date)
                          VALUES(?,?,?,?,?,?) '''
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery, task)
                taskRowId = cursor.lastrowid
            except Error as e:
                print(e)
        else:
            print("Error: Cannot create task when no database exists")

        return taskRowId

    """
    Updates a task based on the given task arguments.

    param task: A list of arguments defining the attributes to be updated and the
                primary key which uniquely identifies the task to be updated.
    return: None  
    """
    def updateTask(self, task):
        if self.db is not None:
            sqlQuery = ''' UPDATE tasks
                           SET priority = ? ,
                               begin_date = ? ,
                               end_date = ?
                           WHERE id = ?'''
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery, task)
            except Error as e:
                print(e)
        else:
            print("Error: Cannot update task when no database exists")

    """
    Deletes a task that matches the given primary key

    param id: The primary key that uniquely identifies a specific task to be deleted
    return: None
    """
    def deleteTask(self, id):
        if self.db is not None:
            sqlQuery = 'DELETE FROM tasks WHERE id=?'
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery, (id,))
            except Error as e:
                print(e)
        else:
            print("Error: Cannot delete a task when no database exists")

    """
    Deletes all tasks in the tasks table

    param: None
    return: None
    """
    def deleteAllTasks(self):
        if self.db is not None:
            sqlQuery = 'DELETE FROM tasks'
            try:
                cursor = self.db.cursor()
                cursor.execute(sqlQuery)
            except Error as e:
                print(e)
        else:
            print("Error: Cannot delete all tasks when no database exists")
    


















        
