from datetime import date, timedelta

class HotelBooking:
    def __init__(self):
        # capacity and room type
        self.room_capacity = {
            'single' : 7, 
            'double' : 3
            }
        

        self.daily_bookings = {} # the data structure for the simple system
        # using dictionary to store data
        # format: { date 1 : { 'single' : 0, 'double' : 0 } }

    def reserve(self, room_type: str, check_in: date, check_out: date, num_rooms: int = 1) -> bool:
        """
        - Main logic function of the booking system 

            room_type : the type of the room -> 'single' or 'double'
            check_in : date to satrt booking 
            check_out : date to be end the booking 
            num_rooms : allow to book mutiple rooms but can be 'optional' to be 1 
            return type : A boolean value to indicate the booking status 

            Main idea : using first loop to check the avaliable, and second loop to reserve the booking 

        """
       # Error handling for room type, dates, and number of the rooms 
        # room_type checking 
        if room_type not in self.room_capacity:
            # Room type have to be "single"or "double"
            raise ValueError("Room Type Error (Room type have to be 'single' or 'double' )")

        # date start and end day check, make sure start < end day
        if check_in >= check_out:
            raise ValueError("check_out date have to after check_in date")

        # Numbers has to be positive
        if num_rooms <= 0:
             raise ValueError("Number of room have to be positive")
        
        # initial the current date to check the availability
        current = check_in
        while current < check_out:
            # get the booking records from the dictionar, {} and 0 handling if it is none
            booked = self.daily_bookings.get(current, {}).get(room_type, 0)
            # if the room over the limit returen False to end 
            if booked + num_rooms > self.room_capacity[room_type]:
                return False  
            current += timedelta(days=1) # add the next day for while to check the nights 

        # Pass the availability check , start reserve the room and update to the system 
        current = check_in # make current to the start date
        while current < check_out:
            if current not in self.daily_bookings:
                # for the new date without any bookings 
                self.daily_bookings[current] = {'single': 0, 'double': 0}
            # start updating bookings
            self.daily_bookings[current][room_type] += num_rooms
            current += timedelta(days=1)# book the next day 
        # retuen True to indicates Success 
        return True
    
    def get_date_status(self, check_date: date) -> dict:
        """
        check_date: date value that need to be check from the dicationary 

        This function return the status of the booking, if NO booking just return '{}'
        """
        status = {} # the return dictionary 
        # get the date query from the bookings data structure
        query = self.daily_bookings.get(check_date, {'single': 0, 'double': 0})

        # Output data processing 
        status["Date"] = check_date # date value
        status["Capacity"] = self.room_capacity # store the capacity 
        
        #get the information for the single room  
        status["Single"] = {"Vacant" : self.room_capacity['single'] - query['single'],
                            "Booked" : query['single']
                            }
        
        #get the information for the double room  
        status["Double"] = {"Vacant" : self.room_capacity['double'] - query['double'],
                            "Booked" : query['double']
                            }

        return status
    
    

    def is_available(self, check_date: date, room_type: str) -> dict:
        """
        Check the availability of a specific room in a certain day 
        
        check_date: date type need to be check
        room_type : string type room that need to check 

        """
        # erorr handling 
        if room_type not in self.room_capacity:
            # Room type have to be "single"or "double"
            raise ValueError("Room Type Error (Room type have to be 'single' or 'double' )")

        #get the room information 
        room = self.daily_bookings.get(check_date, {}).get(room_type, 0)
        #not available -> False
        if room >= self.room_capacity[room_type]:
            return False
        
        # output the room status
        return {
            "Room Type" : room_type,
            "Available" : self.room_capacity[room_type] - room,
            "Booked" : room
        }
    

    def get_total_status(self) -> dict:
        """
        Similar to the get_date_status but return all the reservations 

        No input required, parse the dictionary booking 

        """
        #output data 
        status = {}
      
        # looping all the query data and processing 
        for query in self.daily_bookings:
            #print(query)
            
            query_info = self.daily_bookings.get(query, {}) #reservation information for each date
            query_status = {} # store the info from each day 
            query_status["Capacity"] = self.room_capacity
            # single room 
            query_status["Single"] = {"Vacant" : self.room_capacity['single'] - query_info['single'],
                                           "Booked" : query_info['single']
                                           }
            
            # double room 
            query_status["Double"] = {"Vacant" : self.room_capacity['double'] - query_info['double'],
                                            "Booked" : query_info['double']
                                            }
            # store it to the output 
            status[query] = query_status

        return status

