import pickle
import os
class SystemAdmin:
    def __init__(self):
        self.movies = []
        self.screens = []
        self.time_slots = []

    def add_movie(self,title,screen_number,seats,time_slots):
        movie = Movie(title)
        screen = Screen(screen_number,seats)
        for time_slot in time_slots:
            screen.add_time_slot(TimeSlot(time_slot,seats))
        movie.add_screen(screen)
        self.movies.append(movie)

    def save(self):
        with open('system_admin_info.pkl','wb') as f:
            pickle.dump(self.movies, f)

    def load(self):
        if os.path.exists('system_admin_info.pkl'):
            with open('system_admin_info.pkl','rb') as f:
                self.movies = pickle.load(f)
        else:
            self.movies = []

class User:
    def __init__(self,name,password):
        self.name = name
        self.password = password
        self.bookings = []

    def book_movie(self,system_admin):
        print("Select a movie:")
        for i,movie in enumerate(system_admin.movies):
            print(f"{i+1}. {movie.title}")
        movie_choice = int(input("Select which movie you want to watch: "))- 1
        movie = system_admin.movies[movie_choice]

        print(f"Selected movie: {movie.title}")
        print("Select a time slot:")
        for i,time_slot in enumerate(movie.screen.time_slots):
            print(f"{i+1}. {time_slot.time} ({time_slot.seats_available} seats are currently available) on Screen {movie.screen.screen_number}")
        time_slot_choice = int(input("Select the time slot that you want to choose: ")) - 1
        time_slot = movie.screen.time_slots[time_slot_choice]

        num_seats = int(input("Enter number of seats: "))
        if num_seats > time_slot.seats_available:
            print("Currently, there aren't enough seats available. Try another Timeslot")
            return

        booking = BookingDetails(movie,num_seats,time_slot)
        self.bookings.append(booking)
        time_slot.seats_available = time_slot.seats_available - num_seats
        print(f"You have booked {num_seats} seats for {movie.title} at {time_slot.time}")

    def save(self):
        with open('user_info.pkl','wb') as f:
            pickle.dump(self.bookings, f)

    def load(self):
        if os.path.exists('user_info.pkl'):
            with open('user_info.pkl','rb') as f:
                self.bookings = pickle.load(f)
        else:
            self.bookings = []

class Movie:
    def __init__(self,title):
        self.title = title
        self.screen = None

    def add_screen(self,screen):
        self.screen =screen

    def save_data(self):
        self.screen.save_data()

    def load_data(self):
        self.screen.load_data()

class Screen:
    def __init__(self,screen_number,seats):
        self.screen_number = screen_number
        self.seats = seats
        self.time_slots = []

    def add_time_slot(self,time_slot):
        self.time_slots.append(time_slot)

class TimeSlot:
    def __init__(self,time,seats):
        self.time = time
        self.seats_available = seats

class BookingDetails:
    def __init__(self,movie,num_seats,time_slot):
        self.movie = movie
        self.num_seats = num_seats
        self.time_slot = time_slot

def register_user():
    print("==============================================")
    print("--User Registration--")
    print("Please Enter the Following information")
    name = input("Enter User name: ")
    password = input("Enter User password: ")
    print("==============================================")
    print("\n"*10)
    return User(name,password)
def interface():
    system_admin = SystemAdmin()
    user = register_user()
    system_admin.load()
    user.load()
    while True:
        print("================================================")
        print("1. Admin Menu")
        print("2. Book Movie")
        print("3. Exit Interface")
        choice = int(input("Choose option: "))
        print("================================================")
        if choice == 1:
            print("--LOGIN--")
            admin_password = input("Enter admin password: ")
            if admin_password == "admin":
                while True:
                    print("================================================")
                    print("1. Add movie")
                    print("2. Back")
                    choice = int(input("Choose option: "))
                    print("================================================")
                    if choice == 1:
                        title = input("Enter movie title: ")
                        screen_number = int(input("Enter screen number: "))
                        seats = int(input("Enter number of seats: "))
                        time_slots = []
                        while True:
                            time = input("Enter time slot: ")
                            time_slots.append(time)
                            more_time_slots = input("Do you want to add more timeslots? (yes/no)")
                            if more_time_slots == "no":
                                break
                        system_admin.add_movie(title, screen_number, seats, time_slots)
                    elif choice == 2:
                        break
            else:
                print("Incorrect password")
        elif choice == 2:
            print("Enter password in order to book movie")
            password = input("Enter User password: ")
            print("\n"*10)
            if password == user.password:
                user.book_movie(system_admin)
                user.save()
            else:
                print("Incorrect password")
        elif choice == 3:
            system_admin.save()
            user.save()
            print("Thank you for browsing our website")
            break
interface()
