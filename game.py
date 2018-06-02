# -*- coding: utf-8 -*-
import random;

class Animal:
    def __init__(self,name,hp,x,y):
        self._name = name
        self._health = hp
        self._x = x
        self._y = y
        self._direction = random.randint(1,8)
        self._x_look = x
        self._y_look = y
        self.look()
    def take_hit(self, damage):
        self._health = self._health - damage
    def change_direction(self):
        self._direction = (self._direction + 1) % 8 + 1
    def look(self):
        if self._direction == 1:
            self._x_look = self._x -1
        elif self._direction == 2:
            self._x_look = self._x -1
            self._y_look = self._y +1
        elif self._direction == 3:
            self._y_look = self._y +1    
        elif self._direction == 4:
            self._x_look = self._x +1    
            self._y_look = self._y -1
        elif self._direction == 5:
            self._x_look = self._x +1
        elif self._direction == 6:
            self._x_look = self._x +1
            self._y_look = self._y -1
        elif self._direction == 7:
            self._y_look = self._y -1
        elif self._direction == 8:
            self._x_look = self._x -1
            self._y_look = self._y -1
    def step(self):
        self._x = self._x_look
        self._y = self._y_look
#        self.change_direction()
        self.take_hit(1)
    def eat(self, food, hp_4_food):
        if food > 0:
            self._health += hp_4_food
            return 1
        else:
            return 0

class Herbivore(Animal):
    def __init__(self, name, hp, x, y):
        Animal.__init__(self, name,hp,x,y)
        self._hp_4_food = 2
    def eat(self, food):
        return Animal.eat(self,food,self._hp_4_food)
class Predator(Animal):
    def __init__(self, name, hp, x, y):
        Animal.__init__(self, name,hp,x,y)
        self._hp_4_food = 5
    def eat(self, food):
        return Animal.eat(self,food,self._hp_4_food)

class Field:
    def __init__(self, size_x,size_y):
        self._animal_list = []
        self._field = []
        for i in range(size_x):
            __tmp = []
            for j in range(size_y):
                __tmp.append(Field_cell(i,j))
            self._field.append(__tmp)
    def drop_dead_animals(self):
        for i in range(len(self._field)):
            for j in range(len(self._field[i])):
                for k in range(len(self._field[i][j]._animals)):
                    if self._field[i][j]._animals[k]._health <= 0:
                        self._field[i][j].del_animal(self._field[i][j]._animals[k])
                        self._field[i][j]._meatFood += 2
        self.update_animals()
    def add_animal(self, name, hp, x, y, type):
        if type == 'H':
            self._field[x][y].add_animal(Herbivore(name,hp,x,y))
        elif type == 'P':
            self._field[x][y].add_animal(Predator(name,hp,x,y))    
        self.update_animals()
    def update_animals(self):
        self._animal_list = []
        for i in self._field:
            for j in i:
                if len(j._animals)>0:
                    for animal in j._animals:
                        self._animal_list.append(animal)
                        
    def show_animals(self):
        self.update_animals()
        return self._animal_list    
    def step(self):
        for i in self._animal_list:
            i.eat(self._field[i._x][i._y]._greenFood)
            self._field[i._x][i._y]._greenFood -= 1
        for i in self._animal_list:
            i.look()
        for i in self._animal_list:
            if i._x_look >=0 and i._x_look < len(self._field) and i._y_look >=0 and i._y_look < len(self._field[0]):
                self._field[i._x][i._y].del_animal(i)
                i.step()
                self._field[i._x][i._y].add_animal(i)
            else:
                i.change_direction()
            i.take_hit(1)
        self.drop_dead_animals()
    
class Field_cell:
    def __init__(self, x,y):
        self._x = x
        self._y = y
        self._animals = []
        self._greenFood = random.randint(5,10)
        self._meatFood = 0
    def add_animal(self, animal):
        self._animals.append(animal)
    def del_animal(self, animal):
        self._animals.remove(animal)
    def show_animals_names(self):
        __tmp = []
        for i in self._animals:
            __tmp.append(i._name)
        return __tmp
    
class GameManager:
    def __init__(self, *list):
        self._time = 0
        self._pole = Field(10,10)
        for i in list:
            x = random.randint(0,9)
            y = random.randint(0,9)
            hp = random.randint(1,10) 
            self._pole.add_animal(i, hp, x, y, 'H')
    def show_field(self):
        pass
    def show_animals(self):
        if len(self._pole._animal_list) == 0:
            print("there are no animals on field")
        else:
            for i in self._pole._animal_list:
                print(i._name, i._x, i._y)
    def start_game(self, time):
        for i in range(time):
            self.show_animals()
            self._time += 1
            self._pole.step()

                        
game = GameManager('qwe')
game.start_game(15)

