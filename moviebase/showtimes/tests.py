from faker import Faker
from random import randint
from rest_framework.test import APITestCase, APIRequestFactory
import datetime
from django.utils.timezone import get_current_timezone


from showtimes.models import Cinema, Screening
from movielist.models import Movie, Person


class CinemaTestCase(APITestCase):

    def setUp(self):
        """Populate test database with random data."""
        self.faker = Faker("pl_PL")
        for _ in range(5):
            Cinema.objects.create(name=self.faker.name())

        director = Person.objects.create(name=self.faker.name())

        for _ in range(5):
            Movie.objects.create(title=self.faker.name(),
                                 description=self.faker.text(),
                                 director=director,
                                 year=self.faker.year())

        Screening.objects.create(date="2019-11-07 20:30:00",
                                 cinema_id=randint(0, 5),
                                 movie_id=randint(0, 5))

    def test_post_cinema(self):
        cinemas_before = Cinema.objects.count()
        new_cinema = {
            "name": "name",
            "city": "city",
        }
        response = self.client.post("/cinemas/", new_cinema, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cinema.objects.count(), cinemas_before + 1)
        for key, val in new_cinema.items():
            self.assertIn(key, response.data)
            if isinstance(val, list):
                # Compare contents regardless of their order
                self.assertCountEqual(response.data[key], val)
            else:
                self.assertEqual(response.data[key], val)

    def test_get_cinemas_list(self):
        response = self.client.get("/cinemas/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.count(), len(response.data))

    def test_get_cinema_detail(self):
        response = self.client.get("/cinemas/1/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        for field in ["name", "city", "movies"]:
            self.assertIn(field, response.data)

    def test_delete_cinema(self):
        response = self.client.delete("/cinemas/1/", {}, format='json')
        self.assertEqual(response.status_code, 204)
        cinemas_ids = [cinema.id for cinema in Cinema.objects.all()]
        self.assertNotIn(1, cinemas_ids)

    def test_update_cinema(self):
        response = self.client.get("/cinemas/1/", {}, format='json')
        cinema_data = response.data
        new_name = "Cinema City"
        cinema_data["name"] = new_name
        new_city = "Radom"
        cinema_data["city"] = new_city

        response = self.client.patch("/cinemas/1/", cinema_data, format='json')
        self.assertEqual(response.status_code, 200)
        cinema_obj = Cinema.objects.get(id=1)
        self.assertEqual(cinema_obj.name, new_name)
        self.assertEqual(cinema_obj.city, new_city)

    def test_post_screening(self):
        screenings_before = Screening.objects.count()
        new_screening = {
            "date": "2020-11-07T20:30:00Z",
            "movie": 1,
            "cinema": 1
        }
        response = self.client.post("/screenings/", new_screening, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Screening.objects.count(), screenings_before + 1)
        for key, val in new_screening.items():
            self.assertIn(key, response.data)
            if isinstance(val, list):
                # Compare contents regardless of their order
                self.assertCountEqual(response.data[key], val)
            else:
                self.assertEqual(response.data[key], val)

    def test_get_screenings_list(self):
        response = self.client.get("/screenings/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Screening.objects.count(), len(response.data))

    def test_get_screening_detail(self):
        response = self.client.get("/screenings/1/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        for field in ["date", "movie", "cinema"]:
            self.assertIn(field, response.data)

    def test_delete_screening(self):
        response = self.client.delete("/screenings/1/", {}, format='json')
        self.assertEqual(response.status_code, 204)
        screenings_ids = [screening.id for screening in Screening.objects.all()]
        self.assertNotIn(1, screenings_ids)

    def test_update_screening(self):
        response = self.client.get("/screenings/1/", {}, format='json')
        screening_data = response.data
        new_date = datetime.datetime(2021, 11, 7, 20, 30, tzinfo=get_current_timezone())
        screening_data["date"] = new_date

        new_movie = 3
        screening_data["movie"] = new_movie
        new_cinema = 2
        screening_data["cinema"] = new_cinema

        response = self.client.patch("/screenings/1/", screening_data, format='json')
        self.assertEqual(response.status_code, 200)
        screening_obj = Screening.objects.get(id=1)
        self.assertEqual(screening_obj.date, new_date)
        self.assertEqual(screening_obj.movie.id, new_movie)
        self.assertEqual(screening_obj.cinema.id, new_cinema)
