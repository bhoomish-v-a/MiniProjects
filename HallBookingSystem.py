import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tabulate import tabulate
import mysql.connector
import datetime
from tabulate import tabulate
db = mysql.connector.connect(host="localhost",user="root",password="bhoomi")
cursor = db.cursor()
cursor.execute("USE HallBooking")

class HallBookingApp:
    def __init__(self, master):
        master.geometry('500x500')
        self.master = master
        self.master.title("Hall Booking System")
            
        self.main_frame = tk.Frame(master)
        self.main_frame1 = tk.Frame(master)
        self.book_frame = tk.Frame(master)
        self.remove_frame = tk.Frame(master)
        self.show_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)
 

        # Create label
        self.label = tk.Label(self.main_frame, text="Welcome to Hall Booking System", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Create buttons for halls
        self.button_cs_hall = tk.Button(self.main_frame, text="CS Hall", command=self.toggle_frames1,activebackground="blue")
        self.button_eee_hall = tk.Button(self.main_frame, text="EEE Seminar Hall", command=self.toggle_frames2)
        self.button_mech_hall = tk.Button(self.main_frame, text="Mech Seminar Hall", command=self.toggle_frames3)
        self.button_npt_hall1 = tk.Button(self.main_frame, text="NPT Seminar Hall 1", command=self.toggle_frames4)
        self.button_npt_hall2 = tk.Button(self.main_frame, text="NPT Seminar Hall 2", command=self.toggle_frames5)

        self.button_exit = tk.Button(self.main_frame, text="Exit", command=self.close_window)


        # Pack buttons
        self.button_cs_hall.pack(pady=10)
        self.button_eee_hall.pack(pady=10)
        self.button_mech_hall.pack(pady=10)
        self.button_npt_hall1.pack(pady=10)
        self.button_npt_hall2.pack(pady=10)
        self.button_exit.pack(pady=10)

    def close_window(self):
        self.master.destroy()
    def toggle_frames1(self):
            self.main_frame.pack_forget()
            self.main_frame1.pack(fill="both", expand=True)
            s=self.hall('cs_hall',self.main_frame1,self.main_frame)
    def toggle_frames2(self):
            self.main_frame.pack_forget()
            self.main_frame1.pack(fill="both", expand=True)
            s=self.hall('mech_sem_hall',self.main_frame1,self.main_frame)
    def toggle_frames3(self):
            self.main_frame.pack_forget()
            self.main_frame1.pack(fill="both", expand=True)
            s=self.hall('eee_sem_hall',self.main_frame1,self.main_frame)
    def toggle_frames4(self):
            self.main_frame.pack_forget()
            self.main_frame1.pack(fill="both", expand=True)
            s=self.hall('npt_hall1',self.main_frame1,self.main_frame)
    def toggle_frames5(self):
            self.main_frame.pack_forget()
            self.main_frame1.pack(fill="both", expand=True)
            s=self.hall('npt_hall2',self.main_frame1,self.main_frame)
    class hall:
        def __init__(self,hid,main_frame1,main_frame):
            self.main_frame1=main_frame1
            self.main_frame=main_frame
            self.hid=hid
            print(hid)
            self.button_book = tk.Button(self.main_frame1, text="Book the Hall", command=self.book_hall)
            self.button_remove = tk.Button(self.main_frame1, text="Remove My Booking", command=self.remove_booking)
            self.button_show_booked = tk.Button(self.main_frame1, text="Show Booked Halls", command=self.show_booked_halls)
            self.button_back = tk.Button(self.main_frame1, text="Back", command=self.close_window)

            # Pack buttons
            self.button_book.pack(pady=10)
            self.button_remove.pack(pady=10)
            self.button_show_booked.pack(pady=10)
            self.button_back.pack(pady=10)
        def book_hall(self):
            date = self.get_user_input("Enter a date (YYYY-MM-DD):")
            user_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            session = self.get_user_input("Enter session (FN for morning / AN for afternoon):")
            if(session=='FN'):
                ses=0
            elif(session=='AN'):
                ses=1
            else:
                print("Enter valid session")
                while(session!='AN' and session!='FN'):
                    session=self.get_user_input("Enter session (FN for morning / AN for afternoon):")
                    if(session=='FN'):
                        ses=0
                    elif(session=='AN'):
                        ses=1
            try:
                cursor.execute(f"select date from {self.hid} where date = %s",(date,))
                result1 = cursor.fetchall()
                x=result1[0]
                if (len(result1)):
                    
                    try:
                        cursor.execute(f"select FN,AN from {self.hid} where date = %s",(date,))
                        result2=cursor.fetchall()
                        tup1=result2[0]
                        if(tup1[ses]=='Booked'):
                            print("Already booked")
                            messagebox.showinfo("Booking failed", f"Hall is already booked for {date} of ({session.upper()}) so try another date or session if available")
                            return

                        else:
                            #cursor.execute("UPDATE cs_hall SET {ses} = 'Booked' WHERE date = %s", (date,))
                            #cursor.execute("UPDATE cs_hall SET AN = 'Booked' WHERE date = '2000-10-20'")
                            update_query = f"UPDATE {self.hid} SET `{session}` = 'Booked' WHERE date = %s"
                            cursor.execute(update_query, (date,))
                            db.commit()
                            print("Booked")
                            messagebox.showinfo("Booking Confirmation", f"Hall booked for {date} ({session.upper()})")
                            return

                            
                            
                    except IndexError:
                        print("Error: Index is out of range for the list")
                        
                 
                #date1=x[0].strftime("%Y-%m-%d")

            except mysql.connector.Error as error:
                print("An error occurred:", error)
                messagebox.showinfo("Booking failed", "Hall booking failed)")
            except IndexError:
                #print("Error: Index is out of range for the list")
                self.csBook(date,session)
                messagebox.showinfo("Booking Confirmation", f"Hall booked for {date} ({session.upper()})")
            return
        def csBook(self,date,session):
            if(session=='FN'):
               cursor.execute(f"insert into {self.hid} (date,FN) values(%s,'Booked')",(date,))
            elif(session=='AN'):
               cursor.execute(f"insert into {self.hid} (date,AN) values(%s,'Booked')",(date,))
            db.commit()
            print("Hall booked successfull")

        '''def remove_booking(self):
            date = self.get_user_input("Enter a date (YYYY-MM-DD):")
            user_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            session = self.get_user_input("Enter session (FN for morning / AN for afternoon):")
            while not session or session.upper() not in ['FN', 'AN']:
                session = self.get_user_input("Invaild pls enter crt session (FN for morning / AN for afternoon):")
            update_query = f"UPDATE {self.hid} SET `{session}` = 'Not Booked' WHERE date = %s"
            cursor.execute(update_query, (rdate,))
            db.commit()
            # Perform remove booking operation (replace with your logic)'''
           
        def remove_booking(self):
            # Get user input for date (YYYY-MM-DD format)
            date = self.get_user_input("Enter a date (YYYY-MM-DD):")

            try:
                # Parse the user-provided date string into a datetime.date object
                user_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please enter date in YYYY-MM-DD format.")
                return

            # Get user input for session (FN for morning / AN for afternoon)
            session = self.get_user_input("Enter session (FN for morning / AN for afternoon):")
            while not session or session.upper() not in ['FN', 'AN']:
                session = self.get_user_input("Invalid session. Please enter 'FN' for morning or 'AN' for afternoon:")

            # Construct and execute the SQL query to update the database record
            update_query = f"UPDATE {self.hid} SET `{session.upper()}` = 'Not Booked' WHERE date = %s"
            try:
                cursor.execute(update_query, (user_date,))
                db.commit()
                messagebox.showinfo("Booking Removal", f"Booking removed for {date} ({session.upper()})")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove booking: {e}")
            return

        def show_booked_halls(self):
        
                    try:
                        current_date = datetime.date.today()
                        
                        select_query = f"SELECT * FROM {self.hid} WHERE date >= %s"
                        cursor.execute(select_query, (current_date,))
                        rows = cursor.fetchall()

                        if not rows:
                            messagebox.showinfo("No Bookings", "No bookings found in the database.")
                            return

                        # Create a new Tkinter window to display the results
                        result_window = tk.Toplevel(self.main_frame1)  # Assuming 'master' is the main Tkinter window
                        result_window.title("Available Bookings")

                        # Create a Text widget to display the database query results
                        text_area = tk.Text(result_window, height=10, width=60)
                        text_area.pack(padx=10, pady=10)

                        # Get column names from cursor description
                        column_names = [desc[0] for desc in cursor.description]

                        # Format rows using tabulate and insert into Text widget
                        formatted_rows = tabulate(rows, headers=column_names, tablefmt="grid")
                        text_area.insert(tk.END, formatted_rows)

                    except mysql.connector.Error as error:
                        messagebox.showerror("Database Error", f"Failed to retrieve bookings: {error}")


        def get_user_input(self, prompt):
            return tk.simpledialog.askstring("User Input", prompt)
            

        def close_window(self):
            self.main_frame1.pack_forget()
            self.main_frame.pack(fill="both", expand=True)
            
def main():
    root = tk.Tk()
    
    app = HallBookingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
