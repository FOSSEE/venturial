class dog:
    legs = 4
    cute = True
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def message(self):
        print("I bark at random people")    

Spike = dog("Spike", 2)
print(dog.cute)


# class goldenretriver:
#     cute = "Yes. Very"
#     fur = "Yes A lot"
    
#     def message(self):
        
    