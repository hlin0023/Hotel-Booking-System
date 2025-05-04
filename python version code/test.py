import unittest
import datetime
from main import HotelBooking

class TestBooking(unittest.TestCase):
    def setUp(self):
        self.system = HotelBooking()
        self.today = datetime.date.today()

    def test_capacity(self):
        """
        Test the initial values 
        """
        capacity = self.system.get_date_status(self.today)
        self.assertEqual(capacity['Single']['Vacant'], 7)
        self.assertEqual(capacity['Single']['Booked'], 0)
        
        self.assertEqual(capacity['Double']['Vacant'], 3)
        self.assertEqual(capacity['Double']['Booked'], 0)

    def test_single_booking(self):
        # Book a single room a time 
        self.assertTrue(self.system.reserve("single", self.today, self.today + datetime.timedelta(days=1)))
        booking = self.system.get_date_status(self.today)
        self.assertEqual(booking["Date"], self.today)
        self.assertEqual(booking["Single"]["Vacant"], 6)
        self.assertEqual(booking["Single"]["Booked"], 1)
        # check if double remain unchanged 
        self.assertEqual(booking["Double"]["Vacant"], 3)
        self.assertEqual(booking["Double"]["Booked"], 0)

        # book mutiple single room  a time 
        self.assertTrue(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 2))
        self.assertTrue(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 3))
        self.assertTrue(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 4))
        self.assertTrue(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 5))
        self.assertTrue(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 6))

        # boundary test for over capacity limit 
        self.assertTrue(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 7))
        self.assertFalse(HotelBooking().reserve("single", self.today, self.today + datetime.timedelta(days=1), 8))
    

    def test_double_booking(self):
        # Book a double room a time 
        self.assertTrue(self.system.reserve("double", self.today, self.today + datetime.timedelta(days=1)))
        booking = self.system.get_date_status(self.today)
        self.assertEqual(booking["Date"], self.today)
        self.assertEqual(booking["Single"]["Vacant"],7)
        self.assertEqual(booking["Single"]["Booked"],0)
        # check if single remain unchanged 
        self.assertEqual(booking["Double"]["Vacant"], 2)
        self.assertEqual(booking["Double"]["Booked"], 1)
    
    def test_single_booking_overlap(self):
        # book a single room for 7 time 
        for _ in range(7):
            self.system.reserve("single", self.today, self.today + datetime.timedelta(days=1))
        # try the 8th 
        self.assertFalse(self.system.reserve("single", self.today, self.today + datetime.timedelta(days=1)))
        self.assertFalse(self.system.is_available(self.today, 'single'))


    def test_double_booking_overlap(self):
        # book a single room for 3 time 
        for _ in range(3):
            self.system.reserve("double", self.today, self.today + datetime.timedelta(days=1))
        # try the 4th 
        self.assertFalse(self.system.reserve("double", self.today, self.today + datetime.timedelta(days=1)))
        self.assertFalse(self.system.is_available(self.today, 'double'))

    def test_book_multiple_days(self):
        day1 = self.today
        day2 = self.today + datetime.timedelta(days=5)

        self.assertTrue(self.system.reserve('single', day1, day2))
        self.assertTrue(self.system.reserve('double', day1, day2))

        #check each day from day 1 to day 2 
        for i in range(5):
            book = self.system.get_date_status(self.today + datetime.timedelta(days=i))
            self.assertEqual(book["Double"]["Vacant"], 2)
            self.assertEqual(book["Double"]["Booked"], 1)
            self.assertEqual(book["Single"]["Vacant"],6)
            self.assertEqual(book["Single"]["Booked"],1)
    
    def test_invalid_room_type(self):
        """
        Check all the invalid room types for the function 
        """
        day1 = self.today
        day2 = self.today + datetime.timedelta(days=2)

        with self.assertRaises(Exception):
            self.system.reserve('esuit', day1, day2)
            self.system.reserve('invalid', day1, day2)
            self.system.is_available(self.today, 'invalid')
    
    def test_invalid_room_number(self):
        """
        Room number need to be a positive number
        """
        day1 = self.today
        day2 = self.today + datetime.timedelta(days=2)

        with self.assertRaises(Exception):
            self.system.reserve('single', day1, day2, 0)
            self.system.reserve('single', day1, day2, -1)
            self.system.reserve('double', day1, day2, 0)
    
    def test_invalid_date(self):
        """
        Dates start time and end time need to in a order 
        """
        day1 = self.today
        day2 = self.today + datetime.timedelta(days=2)

        with self.assertRaises(Exception):
            self.system.reserve('single', day2, day1)
            self.system.reserve('double', day2, day1)

    def test_get_date_status(self):
        """
        Tets the date status getter to return correct output 
        """
        day1 = self.today
        day2 = self.today + datetime.timedelta(days=10)
        self.system.reserve('single', day1, day2)
        self.system.reserve('double', day1, day2, 3)

        for i in range(10):
            book = self.system.get_date_status(self.today + datetime.timedelta(days=i))
            self.assertEqual(book["Double"]["Vacant"], 0)
            self.assertEqual(book["Double"]["Booked"], 3)
            self.assertEqual(book["Single"]["Vacant"],6)
            self.assertEqual(book["Single"]["Booked"],1)

    def test_is_available(self):
        """
        testing the function of the  is_available(), checking for a room type in a day 
        """
        day1 = self.today
        day2 = self.today + datetime.timedelta(days=10)
        self.system.reserve('single', day1, day2, 7)
        self.system.reserve('double', day1, day2, 3)

        for i in range(10):
            self.assertFalse(self.system.is_available(self.today + datetime.timedelta(days=i), 'single'))
            self.assertFalse(self.system.is_available(self.today + datetime.timedelta(days=i), 'double'))


    def test_get_total_status(self):
        """
        testing the function of the  get_total_status() by checking the length of the dictionary 
    
        """
        # checking for the empty booking 
        self.assertEqual(self.system.get_total_status(), {})

        day1 = self.today
        day2 = self.today + datetime.timedelta(days=10)
        self.system.reserve('single', day1, day2)
        status = self.system.get_total_status()
        self.assertEqual(len(status), 10)




if __name__ == '__main__':
    unittest.main()