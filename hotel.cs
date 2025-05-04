using System;
using System.Collections.Generic;
using System.Linq;
using HotelReservation.Models;

namespace HotelReservation.Services
{
    public class Hotel
    {
        private readonly Dictionary<RoomType, int> _capacity = new Dictionary<RoomType, int>
        {
            { RoomType.Single, 7 },
            { RoomType.Double, 3 }
        };

        private readonly List<Booking> _bookings = new List<Booking>();

        public bool BookRoom(RoomType type, DateTime checkIn, DateTime checkOut)
        {
            if (!IsAvailable(type, checkIn, checkOut))
                return false;

            _bookings.Add(new Booking(type, checkIn, checkOut));
            return true;
        }

        public bool IsAvailable(RoomType type, DateTime checkIn, DateTime checkOut)
        {
            var date = checkIn.Date;
            while (date < checkOut.Date)
            {
                var count = _bookings.Count(b => b.Type == type && b.Overlaps(date, date.AddDays(1)));
                if (count >= _capacity[type])
                    return false;
                date = date.AddDays(1);
            }
            return true;
        }

        public IDictionary<RoomType, (int Booked, int Vacant)> GetStatusForDate(DateTime date)
        {
            var status = new Dictionary<RoomType, (int, int)>();

            foreach (var kv in _capacity)
            {
                var type = kv.Key;
                var booked = _bookings.Count(b => b.Type == type && b.Overlaps(date.Date, date.Date.AddDays(1)));
                var vacant = kv.Value - booked;
                status[type] = (booked, vacant);
            }

            return status;
        }
    }
}
