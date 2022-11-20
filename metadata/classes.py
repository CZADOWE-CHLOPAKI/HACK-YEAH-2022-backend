class Sender:
    def __init__(self, name, adres, email, ePUAP):
        self.name = name
        self.adres = adres
        self.email =  email
        self.ePUAP = ePUAP
    
    def __str__(self) -> str:
        return f"name -> {self.name}\nadres -> {self.adres}\nemail -> {self.email}\nePUAP -> {self.ePUAP}\n"

class Receiver:
    def __init__(self, name, address, pesel=None, nip=None):
        self.name = name
        self.address = address
        self.pesel = pesel
        self.nip = nip

    def __str__(self) -> str:
        return f"name -> {self.name}\naddress -> {self.address}\nPESEL -> {self.pesel}\nNIP -> {self.nip}"

class Document:
    def __init__(self, number, unp, date, signee):
        self.number = number
        self.unp = unp
        self.date = date
        self.signee = signee

    def __str__(self) -> str:
        return f"number -> {self.number}\nunp -> {self.unp}\ndate -> {self.date}\nsignee -> {self.signee}"