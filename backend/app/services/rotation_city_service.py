from app.models.rotation_city import RotationCity


class RotationCityService:
    @staticmethod
    def get_rotation_cities():

        cities = RotationCity.query.all()

        return cities