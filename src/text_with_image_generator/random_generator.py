import random
import datetime

ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
abc = 'abcdefghijklmnopqrstuvwxyz'
numbers = '123456789'

color_list = ['#7E0EE1', '#E10E7E']

class RandomGenerator():

    def randomName(self, length=10):
        name = random.choice(ABC)

        for i in range(length - 1):
            character_type = random.choice([abc, numbers])
            name += random.choice(character_type)
            date_objc = datetime.date.today()
            formatted_date = date_objc.strftime('%m-%d-%Y')
            name_date = f'{name}_{formatted_date}'

        return name_date

    def randomHexCode(self):
        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        return color[0]

    def randomColor(self):
        color = random.choice(color_list)
        return color
