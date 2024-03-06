from database.databaseManager import DatabaseManager

def create_tables():
    db_manager = DatabaseManager()
    db_manager.connect()

    create_users_table = """
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        hashed_password VARCHAR(255) NOT NULL,
        phone_number VARCHAR(50) default '010-0000-0000',
        user_role VARCHAR(50) NOT NULL DEFAULT 'customer'
    );
    """

    create_movies_table = """
    CREATE TABLE Movies (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        director VARCHAR(100),
        runtime INT,
        genre VARCHAR(50),
        release_date DATE,
        description TEXT,
        rating DECIMAL(3, 1),
        booking_rate DECIMAL(5, 2),
        price DECIMAL(10, 2) NOT NULL
    );
    """

    create_screens_table = """
    CREATE TABLE Screens (
        screen_id SERIAL PRIMARY KEY,
        screen_number INT NOT NULL,
        seat_capacity INT NOT NULL
    );
    """

    create_screenings_table = """
    CREATE TABLE Screenings (
        screening_id SERIAL PRIMARY KEY,
        screen_id INT NOT NULL,
        movie_id INT NOT NULL,
        screening_start_time TIMESTAMP NOT NULL,
        screening_end_time TIMESTAMP NOT NULL,
        CONSTRAINT fk_screen FOREIGN KEY (screen_id) REFERENCES Screens(screen_id),
        CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
    );
    """

    create_seats_table = """
    CREATE TABLE Seats (
        seat_id SERIAL PRIMARY KEY,
        screen_id INT NOT NULL,
        screening_id INT not null,
        seat_number VARCHAR(10) NOT NULL,
        is_available BOOLEAN NOT NULL DEFAULT TRUE,
        CONSTRAINT fk_screen FOREIGN KEY (screen_id) REFERENCES Screens(screen_id),
        CONSTRAINT fk_screening FOREIGN KEY (screening_id) REFERENCES Screenings(screening_id)
    );
    """

    create_reservations_table = """
    CREATE TABLE Reservations (
        reservation_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        screening_id INT NOT NULL,
        seat_id INT NOT NULL,
        reservation_time TIMESTAMP NOT NULL,
        payment_status BOOLEAN NOT NULL,
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
        CONSTRAINT fk_screening FOREIGN KEY (screening_id) REFERENCES Screenings(screening_id),
        CONSTRAINT fk_seat FOREIGN KEY (seat_id) REFERENCES Seats(seat_id)
    );
    """

    create_ratings_table = """
    CREATE TABLE Ratings (
        rating_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        rating DECIMAL(2, 1) NOT NULL,
        rating_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
        CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
        CONSTRAINT chk_rating CHECK (rating >= 0 AND rating <= 10.00)
    );
    """

    create_advertisements_table = """
    CREATE TABLE Advertisements (
        advertisement_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
        CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
    );
    """

    try:
        db_manager.execute_action_query(create_users_table)
        db_manager.execute_action_query(create_movies_table)
        db_manager.execute_action_query(create_screens_table)
        db_manager.execute_action_query(create_screenings_table)
        db_manager.execute_action_query(create_seats_table)
        db_manager.execute_action_query(create_reservations_table)
        db_manager.execute_action_query(create_ratings_table)
        db_manager.execute_action_query(create_advertisements_table)
        print("All tables created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    create_tables()