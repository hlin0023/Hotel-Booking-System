using System;
using HotelReservation.Models;

namespace HotelReservation.Models
{
    public class Booking
    {
        public RoomType Type { get; }
        public DateTime CheckIn { get; }
        public DateTime CheckOut { get; }

        public Booking(RoomType type, DateTime checkIn, DateTime checkOut)
        {
            if (checkIn.Date >= checkOut.Date)
                throw new ArgumentException("Check-out date must be after check-in date");

            Type = type;
            CheckIn = checkIn.Date;
            CheckOut = checkOut.Date;
        }

        public bool Overlaps(DateTime otherCheckIn, DateTime otherCheckOut)
        {
            return !(CheckOut <= otherCheckIn || CheckIn >= otherCheckOut);
        }
    }
}
