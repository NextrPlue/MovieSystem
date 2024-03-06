from systems.loginSystem import LoginSystem
from systems.movieManagementSystem import MovieManagementSystem
from systems.screenManagementSystem import ScreenManagementSystem
from systems.cinemaScheduleSystem import CinemaScheduleSystem
from systems.movieBookingSystem import MovieBookingSystem
from systems.bookingInquirySystem import BookingInquirySystem

def create_test_data():
    try:
        # 사용자 생성
        system = LoginSystem()
        system.create_user('관리자 산지니', 'admin', 'admin', None, 'admin')
        system.create_user('사용자 산지니', 'customer', 'customer')
        system.create_user('배급사 산지니', 'distributor', 'distributor', None, 'distributor')
        system.create_user('Jane Smith', 'janesmith@example.com', 'password')
        system.create_user('Alice Johnson', 'alicej@example.com', 'password')
        system.create_user('Carol Davis', 'carold@example.com', 'password')
        system.create_user('David Evans', 'davide@example.com', 'password')
        system.create_user('Eve Foster', 'evef@example.com', 'password')
        system.create_user('Frank Green', 'frankg@example.com', 'password')
        system.create_user('John Doe', 'johndoe@example.com', 'password')
        system.create_user('Bob Brown', 'bobb@example.com', 'password')
        system.close()

        # 영화 생성
        system = MovieManagementSystem()
        system.add_movie('The Shawshank Redemption', 
                        'Frank Darabont',
                        142,
                        'Drama',
                        '1994-09-23',
                        'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                        10.50)
        system.add_movie('Forrest Gump',
                        'Robert Zemeckis',
                        142,
                        'Drama',
                        '1994-07-06',
                        'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
                        9.50)
        system.add_movie('Inception',
                        'Christopher Nolan',
                        148,
                        'Sci-Fi',
                        '2010-07-16',
                        'A thief who steals corporate secrets through the use of dream-sharing technology.',
                        10.00)
        system.add_movie('Pulp Fiction',
                        'Quentin Tarantino',
                        154,
                        'Crime',
                        '1994-10-14',
                        'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                        11.00)
        system.add_movie('The Matrix',
                        'Lana Wachowski, Lilly Wachowski',
                        136,
                        'Action',
                        '1999-03-31',
                        'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                        12.00)
        system.add_movie('Parasite',
                        'Bong Joon-ho',
                        132,
                        'Drama',
                        '2019-05-30',
                        'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
                        13.00)
        system.add_movie('Fight Club',
                        'David Fincher',
                        139,
                        'Drama',
                        '1999-10-15',
                        'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.',
                        14.00)
        system.add_movie('Interstellar',
                        'Christopher Nolan',
                        169,
                        'Sci-Fi',
                        '2014-11-07',
                        "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                        15.00)
        system.close()

        # 상영관 생성
        system = ScreenManagementSystem()
        system.add_screen(1, 100)
        system.add_screen(2, 150)
        system.add_screen(3, 200)
        system.add_screen(4, 120)
        system.add_screen(5, 130)
        system.add_screen(6, 140)
        system.add_screen(7, 110)
        system.add_screen(8, 160)
        system.close()

        # 상영정보 생성
        system = CinemaScheduleSystem()
        system.add_screening(1, 1, '2023-01-01 14:00:00', '2023-01-01 16:30:00')
        system.add_screening(1, 2, '2023-01-02 17:00:00', '2023-01-02 19:30:00')
        system.add_screening(2, 3, '2023-01-03 20:00:00', '2023-01-03 22:30:00')
        system.add_screening(2, 4, '2023-01-04 23:00:00', '2023-01-05 01:30:00')
        system.add_screening(1, 5, '2023-01-05 10:00:00', '2023-01-05 12:30:00')
        system.add_screening(1, 6, '2023-01-06 13:00:00', '2023-01-06 15:30:00')
        system.add_screening(2, 7, '2023-01-07 16:00:00', '2023-01-07 18:30:00')
        system.add_screening(2, 8, '2023-01-08 19:00:00', '2023-01-08 21:30:00')
        system.close()

        system = MovieBookingSystem()
        system.book_movie(4, 1, 2)
        system.book_movie(4, 3, 204)
        system.book_movie(5, 2, 106)
        system.book_movie(5, 6, 606)
        system.book_movie(6, 6, 614)
        system.book_movie(7, 8, 854)
        system.book_movie(8, 7, 706)
        system.book_movie(8, 5, 533)
        system.book_movie(9, 3, 226)
        system.book_movie(10, 6, 615)
        system.book_movie(10, 2, 113)
        system.book_movie(11, 6, 626)
        system.update_booking_rate()
        system.close()

        system = BookingInquirySystem()
        system.add_movie_rating(4, 1, 8.5)
        system.add_movie_rating(4, 3, 9.4)
        system.add_movie_rating(5, 2, 7.8)
        system.add_movie_rating(5, 6, 9.7)
        system.add_movie_rating(6, 6, 9.8)
        system.add_movie_rating(7, 8, 8.9)
        system.add_movie_rating(8, 5, 8.6)
        system.add_movie_rating(8, 7, 7.9)
        system.add_movie_rating(9, 3, 8.7)
        system.add_movie_rating(10, 6, 9.6)
        system.add_movie_rating(10, 2, 9.4)
        system.add_movie_rating(11, 6, 8.9)
        system.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_test_data()