# This is an Car Class Program

class Car:
    def __init__ (self,brand,model,color):
        self.brand=brand
        self.model=model
        self.color=color
        
    def start(self):
        print(f"{self.brand} is Starting")
        
    def stop(self):
        print(f"{self.model} is Stopping")
        
    def detail(self):
        print(f"Brand : {self.brand}")
        print(f"Model : {self.model}")
        print(f"Color : {self.color}")
        
c1=Car("Toyota","corolla","White")
c2=Car("Honda","civic","Black")

c1.detail()
c1.start()
print()
c2.detail()
c2.stop()