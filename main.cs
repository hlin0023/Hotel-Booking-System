using System;
using HotelReservation.Models;
using HotelReservation.Services;

namespace HotelReservation
{
    class Program
    {
        static void Main(string[] args)
        {
            var hotel = new Hotel();
            var checkIn = DateTime.Today.AddDays(1);
            var checkOut = checkIn.AddDays(2);

            bool booked = hotel.BookRoom(RoomType.Single, checkIn, checkOut);
            Console.WriteLine(booked ? "Booking successful!" : "Booking failed.");

            var status = hotel.GetStatusForDate(checkIn);
            foreach (var kv in status)
            {
                Console.WriteLine($"{kv.Key}: Booked={kv.Value.Booked}, Vacant={kv.Value.Vacant}");
            }
        }
    }
}