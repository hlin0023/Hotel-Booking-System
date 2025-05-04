# Hotel Reservation System

## The Python folder is the python version of the code but in a simpler way. 

A simple C# solution for managing hotel room bookings in memory.  
This project consists of three libraries and one test project:

- **HotelReservation.Models**  
  Defines `RoomType` and `Booking`.

- **HotelReservation.Services**  
  Implements `Hotel`, which handles availability, booking, and status.

- **HotelReservation**  
  (Optional) Console app with `Program.cs` demonstrating basic usage.

- **HotelReservation.Tests**  
  NUnit test project validating expected behaviors and edge cases.

## Requirements

- [.NET 6.0 SDK](https://dotnet.microsoft.com/download/dotnet/6.0)

## Setup & Build

1. Clone or download the repo.
2. From the root folder, run:
   ```sh
   dotnet build
