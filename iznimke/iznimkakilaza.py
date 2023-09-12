class IznimkaKilaza(Exception):
    def __init__(self):
        super(IznimkaKilaza, self).__init__('Korisniku se preporučuje posjet doktoru zbog kilaže!')