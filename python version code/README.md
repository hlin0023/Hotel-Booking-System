# Simple Hotel Booking System

## Design decisions:


## 1. Core design for the `reserve()`:
- **Booking system's atomicity**: using first loop to check the available, and second loop to reserve the booking

Solutions | Advantages | Disadvantages | Reasons for final selection
--- | --- | --- | --- 
**Check before updating-Two Loop (currently)** | **Simple code - Avoid dirty data** |Traverse the date twice | Simple implementation, Clear logic -> Meet requirement
Transaction lock mechanism| High concurrency safety | Increase complexity | No concurrency required for this project  
Optimistic lock | High performance | Rollback logic needs to be processed | Over-design -> for complex system


## 2. The number of rooms can be specified: 
    multiple rooms (of the same type) can be booked at a Multiple rooms (of the same type) can be booked at a time. For example, 2 single rooms can be reserved at a time if available.

    The number of rooms "num_room" can be optional, which means that if not entered, it will be 1 for the reservation.
    "num_rooms: int = 1", if this attribute is entered it can be any number.

### Room type structure  

Solutions | Advantages | Disadvantages | Reasons for final selection
--- | --- | --- | --- 
**Hard-coded room types (currently)** | **Simple code** |Extension requires code modification | Simple implementation, meets core requirements 
Dynamic addition of dictionary| Flexible extension | Cannot delete room types | No complex functions rquired for this project  
Room type configuration class | Support more metadata (such as price) and OOP | Increase complexity | Over-design -> for complex system


## 3. Date range (nights) : 
    Check-in date (inclusive) to check-out date (exclusive), ask for the date instead of the nights. 
    Eg. 15 March to 20 March 2025 covers 4 days.

## 4. Data storage(Dictionary): 
     Use a dictionary "daily_bookings" to track the number of reservations by each day, and only record the dates with reservations to save memory.

    with the structure of { date: {
        'single': number of bookings, 
        'double': number of bookings
                                    }
                            }.

    advantages: Quick query of daily status, simple implementation. 
    
    Disadvantages: Long-term booking requires traversing all dates.

Solutions | Advantages | Disadvantages | Reasons for final selection
--- | --- | --- | --- 
**Store by day (current method dictionary)** | **Quickly query the status of a certain day (O(1))** | Long-term booking check efficiency is low | Simple implementation, meets core requirements 
Store by booking record(Using List) | easy for cancel/modify operations | Querying daily status requires traversing all records | No complex functions rquired for this project  
Hybrid storage | Balance query and operation efficiency | High implementation complexity | Over-design

**--> But for this project, not really require a long-term booking, if so database is required** 

    Storage for the booking records is also doable.
    Like storing each query booking information in the data storage. 

    For example: store the check-in_day and check-out day and room type for each booking.
    However this method requires extra time for checking for the overlaps and availability of rooms. As this project is just a small data set, using a dictionary increases the efficiency. 

**Data is only stored in memory and will be lost after restart**

## 5. Invalid request handling: 
     Invalid room type, zero rooms, and invalid date range(check out is earlier than check-in) directly return failure or raise an Error me
    
    Boundary processing: 
    1. Invalid room types are rejected directly
    2. Start date >= end date is considered invalid
 

## 6. Concurrency : 
     No concurrency is considered in this system, it is only suitable for a single-threaded environment. 
    As it is a simple system, for further development, some methods like Redis and message queues can be used for the system.

## 7. getters : 
     3 types of the getter are used:
        get_date_status: this is getting all status for a date
        is_available: checking a room type is available at one date
        get_total_status: return all bookings 

# Time spent
    About 3 hours, including design, coding, testing and documentation.

# Trade-offs

## 1. Efficiency and simplicity: 
 -> **Simplicity vs. scalability**
Choose simplicity for this project, **prioritize the core requirements** 

choose to traverse daily instead of complex period overlap checks, although it is less efficient for long date ranges, but it is simple to implement. 

## 2. Memory efficiency vs query performance
Choose a compromise: store by day to balance the two. If we store 10-day reservations for current system only 10 records in the dictionary. But the the query booking storage, it might consits many.

For example:
Store 10-day reservations for 2 room types → 10 records
{day1:{...}, day2:{...}, ...., day10:{...}}

Change to store by reservation record → possibly hundreds of records 

## 3. Functional limitations: 
    does not support cancellation/modification of reservations. 
    -> can be done by simply adding a setter to modify the dictionary.


## 3. Extensibility: 
    The current design is easy to expand the room type or number of rooms ->(by adding room type to the capacity), but adding new features requires adjusting the structure


# How to Run
1. Ensure that `main.py` ad `test.py` are in the same directory.
2. Run the `test.py` directly or python -m unittest test.py 

# Test coverage
1. Basic functions: initial status verification, valid reservation
2. Border cases: overbooking, invalid room type, zero room request, invalid date
3. Extended functions: dynamically add room types, mixed or mutiple room types at the same time
# Future Improvement

1. Design Part 

    This project only uses one class to implement the system, the system can be more **Object-Oriented** by separating the project into the class **Room **, the class **Booking**, and the class **System**.  

    Room class (**Encapsulate basic room information [type, total quantity]**) only handles the room type and room number, some setter and getter can be included to modify the room for extension.  

    Booking class (**Record details of each booking**) handle the reservation, and stores each transaction, this will be stored like a query booking records  

    System class(**Manage all room types and reservation records and provide extension interface**) will be performing all the methods together, including bookings, cancellations.

2. Cancel booking feature 
3. For testing include the **date validation** including wrong dates and date formats. However, this project did not request mannual input, just using `date()` method 


