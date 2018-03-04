from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json

from ..models import Game, Genre


class GameTestCase(TestCase):
    
    def testCreatingGame(self):
        genre = Genre.objects.create(name="FPS")
        developer = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        Game.objects.create(name="GTA", description="Exciting game...", price=10.0, url="http://www.gta.com", genreID=genre, developerID=developer)
        testgame = Game.objects.get(name="GTA")
        self.assertEqual(testgame.name, "GTA", "Getting a just created game")

    def _testfieldtype(self, model, modelname, fieldname, type):
        try:
          field = model._meta.get_field(fieldname)
          self.assertTrue(isinstance(field, type), "Testing the type of %s field in model %s"%(fieldname, modelname))
        except FieldDoesNotExist:
          self.assertTrue(False, "Testing if field %s exists in model %s"%(fieldname, modelname))
        return field

    def testFieldTypes(self):
      self._testfieldtype(Game, 'Game', 'gameID', models.AutoField)
      self._testfieldtype(Game, 'Game', 'name', models.CharField)
      self._testfieldtype(Game, 'Game', 'description', models.TextField)
      self._testfieldtype(Game, 'Game', 'price', models.FloatField)
      self._testfieldtype(Game, 'Game', 'publishDate', models.DateTimeField)
      self._testfieldtype(Game, 'Game', 'url', models.URLField)
      self._testfieldtype(Game, 'Genre', 'genreID', models.ForeignKey)
      self._testfieldtype(Game, 'User', 'developerID', models.ForeignKey)
      self._testfieldtype(Game, 'Game', 'image', models.ImageField)


    def testModelOrdering(self):
        prev = None

        # Check both Continent and Country classes
        for ModelClass in (Game,):

            # Iterate over all objects and check that the next is greater than the previous
            for cur in ModelClass.objects.all():
                if prev:
                    self.assertTrue(prev.name < cur.name, "Checking ordering of objects in " + cur.__class__.__name__ + ". Did you remember to set the default ordering?")
                prev = cur
            prev = None

'''
class JsonTestCase(TestCase):
    fixtures = ['countrydata.xml']

    def setUp(self):
        """ Initializes the Django test client before each test """
        self.client = Client()

    def _url(self, continent_code, country_code=None):
        if not country_code:
            return reverse('continent-json', args=[continent_code])
        return reverse('country-json', args=[continent_code, country_code])

    def testJsonContinents(self):
        for continent in Continent.objects.all():
            response = self.client.get(self._url(continent.code))
            self.assertEquals(response.status_code, 200, "Testing JSON continent request status code.")
            country_dict = json.loads(response._container[0].decode(encoding="utf-8"))

            # Check that each country name can be found under the corresponding code in dict
            for country in continent.countries.all():
                self.assertEquals(country.name, country_dict[country.code])

    def testJsonCountries(self):
        for country in Country.objects.all():
            response = self.client.get(self._url(country.continent.code, country.code))
            self.assertEquals(response.status_code, 200, "Testing JSON country request status code.")

            fields = json.loads(response._container[0].decode(encoding="utf-8"))

            # Check that each field can be found in fields dict
            self.assertEquals(country.population, fields["population"])
            self.assertEquals(country.area, fields["area"])
            self.assertEquals(country.capital, fields["capital"])

    def testJsonCallback(self):
        response = self.client.get(self._url('eu', 'no'), {"callback": "custom_callback"})
        self.assertContains(response, "custom_callback(")
        response = self.client.get(self._url('eu'), {"callback": "trigger"})
        self.assertContains(response, "trigger(")

    def testInvalidParameters(self):

        # Norway should not be found under North America
        response = self.client.get(self._url('na', 'no'))
        self.assertEquals(response.status_code, 404, "Looking for a real country in a wrong continent.")

        # There is no country "xx" in North America
        response = self.client.get(self._url('na', 'xx'))
        self.assertEquals(response.status_code, 404, "Looking for a non existent country in a real continent.")

        # There is no continent with a "xx" code
        response = self.client.get(self._url('xx', 'fi'))
        self.assertEquals(response.status_code, 404, "Looking for a real country in a non existent continent.")

        # Norway should be found under Europe
        response = self.client.get(self._url('eu', 'no'))
        self.assertEquals(response.status_code, 200, "Testing valid request status code.")
        '''
