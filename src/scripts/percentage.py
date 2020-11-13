class Percentage:
    # default values for gaming type pc
    gpu = 33
    cpu = 22
    ram = 10
    motherboard = 12
    ssd = 10
    hdd = 5
    psu_and_case = 8

    def __init__(self, gpu = gpu, cpu = cpu, ram = ram, motherboard = motherboard, ssd = ssd, hdd = hdd, psu_and_case = psu_and_case):
        self.gpu = gpu
        self.cpu = cpu
        self.ram = ram
        self.motherboard = motherboard
        self.ssd = ssd
        self.hdd = hdd
        self.psu_and_case = psu_and_case
