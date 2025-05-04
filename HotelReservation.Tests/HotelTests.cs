using System;
using NUnit.Framework;
using HotelReservation.Models;
using HotelReservation.Services;

namespace HotelReservation.Tests
{
    public class HotelTests
    {
        private Hotel _hotel;
        private DateTime _today;

        [SetUp]
        public void Setup()
        {
            _hotel = new Hotel();
            _today = DateTime.Today;
        }

        [Test]
        public void SuccessfulSingleBooking_ReducesVacancy()
        {
            var checkIn = _today.AddDays(1);
            var checkOut = checkIn.AddDays(2);

            Assert.IsTrue(_hotel.BookRoom(RoomType.Single, checkIn, checkOut));
            var (booked, vacant) = _hotel.GetStatusForDate(checkIn)[RoomType.Single];
            Assert.AreEqual(1, booked);
            Assert.AreEqual(6, vacant);
        }

        [Test]
        public void OverbookingSingle_ReturnsFalse()
        {
            var checkIn = _today.AddDays(1);
            var checkOut = checkIn.AddDays(1);
            for (int i = 0; i < 7; i++)
                Assert.IsTrue(_hotel.BookRoom(RoomType.Single, checkIn, checkOut));
            Assert.IsFalse(_hotel.BookRoom(RoomType.Single, checkIn, checkOut));
        }

        [Test]
        public void NonOverlappingBookings_Allowed()
        {
            var checkIn1 = _today.AddDays(5);
            var checkOut1 = checkIn1.AddDays(2);
            var checkIn2 = checkOut1;
            var checkOut2 = checkIn2.AddDays(2);

            Assert.IsTrue(_hotel.BookRoom(RoomType.Single, checkIn1, checkOut1));
            Assert.IsTrue(_hotel.BookRoom(RoomType.Single, checkIn2, checkOut2));
        }

        [Test]
        public void InvalidDateRange_ThrowsException()
        {
            Assert.Throws<ArgumentException>(() => new Booking(RoomType.Single, _today.AddDays(2), _today.AddDays(1)));
        }

        [Test]
        public void DoubleRoomBooking_AcrossMultipleNights()
        {
            var checkIn = _today.AddDays(3);
            var checkOut = checkIn.AddDays(3);

            Assert.IsTrue(_hotel.BookRoom(RoomType.Double, checkIn, checkOut));
            for (var date = checkIn; date < checkOut; date = date.AddDays(1))
            {
                var (booked, vacant) = _hotel.GetStatusForDate(date)[RoomType.Double];
                Assert.AreEqual(1, booked);
                Assert.AreEqual(2, vacant);
            }
        }
    }
}