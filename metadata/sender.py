class Sender:
    def __init__(self, name, adres, email, ePUAP):
        self.name = name
        self.adres = adres
        self.email =  email
        self.ePUAP = ePUAP
    
    def __str__(self) -> str:
        return f"name -> {self.name}\nadres -> {self.adres}\nemail -> {self.email}\nePUAP -> {self.ePUAP}\n"