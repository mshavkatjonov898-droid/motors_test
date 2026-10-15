import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='../projects/app.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Avto:
    __jami = 0

    def __init__(self, model, narx, egasi=None, rang="oq"):
        self.egasi = egasi
        self.model = model
        self.narx = narx
        self.rang = rang
        Avto.__jami += 1

    @classmethod
    def jami_yaratilgan(cls):
        return cls.__jami

    def __str__(self):
        return self.get_info()

    def __gt__(self, other):
        return self.narx > other.narx

    def get_info(self):
        if self.egasi is None:
            return f"🚗 {self.rang} {self.model} - {self.narx}$ (sotuvda)"
        return f"🚗 {self.rang} {self.model} - {self.narx}$ (Egasi: {self.egasi.ism})"


class Mijoz:
    def __init__(self, ism, tel):
        self.ism = ism
        self.tel = tel


class ElektroAvto(Avto):
    # Добавлен egasi=None по умолчанию
    def __init__(self, zaryad_km, model, narx, egasi=None, rang="oq"):
        super().__init__(model, narx, egasi, rang)
        self.zaryad_km = zaryad_km

    def get_info(self):
        if self.egasi is None:
            return f"⚡ {self.rang} {self.model} - {self.narx}$ | zaryad: {self.zaryad_km} km (sotuvda)"
        return f"⚡ {self.rang} {self.model} - {self.narx}$ | zaryad: {self.zaryad_km} km (Egasi: {self.egasi.ism})"


class Salon:
    def __init__(self, nom):
        self.nom = nom
        self.__avtolar = []

    def __len__(self):
        return len(self.__avtolar)

    def __getitem__(self, index):
        return self.__avtolar[index]

    def add(self, avto):
        self.__avtolar.append(avto)
        return f"Salonga qo'shildi: {avto.rang} {avto.model} — {avto.narx}$ (sotuvda)"

    def add_e(self, avto):
        self.__avtolar.append(avto)
        return f"Salonga qo'shildi: {avto.rang} {avto.model} — {avto.narx}$ | zaryad: {avto.zaryad_km} km (sotuvda)"

    def hammasi(self):
        for avto in self.__avtolar:
            print(avto.get_info())

    def sotuvda(self):
        return [car for car in self.__avtolar if car.egasi is None]

    def eng_qimmat(self):
        sotuvdagi_avtolar = self.sotuvda()
        if not sotuvdagi_avtolar:
            return None
        return max(sotuvdagi_avtolar)

    def sot(self, raqam, mijoz):
        try:
            if raqam < 1:
                raise IndexError
            avto = self.__avtolar[raqam - 1]
            if avto.egasi is not None:
                print("Afsus, allaqachon sotilgan")
            else:
                avto.egasi = mijoz
                print("SOTILDI!")
        except IndexError:
            print("Noto'g'ri raqam")

    def saqla(self):
        with open("../lesson/salon.txt", "w") as file:
            for avto in self.__avtolar:
                file.write(f"{avto.get_info()}\n")
        print("Malumotlar faylga saqlandi.")

    def yukla(self):
        try:
            with open("../lesson/salon.txt", "r") as file:
                content = file.read()
                print("--- Fayldan yuklangan ma'lumotlar ---")
                print(content if content else "Fayl bo'sh.")
        except FileNotFoundError:
            print("Fayl topilmadi. Avval ma'lumotlarni saqlang.")

    def search(self, soz):
        soz = soz.lower()
        return [_ for _ in self.__avtolar if soz in _.model.lower() or soz in _.rang.lower()]

if __name__ == "__main__":
    my_salon = Salon("UStudy Motors")
    while True:
        print(f"""\n===== {my_salon.nom} | avtolar: {len(my_salon)} =====
    1. Avto qo'shish
    2. Elektromobil qo'shish
    3. Hammasini ko'rish
    4. Sotish
    5. Eng qimmat avto
    6. Faylga saqlash
    7. Fayldan yuklash
    0. Chiqish
    """)
        tanlov = input("Tanlang: ")
        if tanlov == '1' or tanlov == '2':
            model = input("Modelni kiriting: ")

            while True:
                try:
                    narx = int(input("Narxni kiriting: "))
                    break
                except ValueError:
                    print("Iltimos, narxni faqat son bilan kiriting!")

            rang = input("Rangini kiriting (bo'sh qoldirsangiz standart): ")

            if tanlov == '1':
                if rang == "":
                    avto = Avto(model, narx)
                else:
                    avto = Avto(model, narx, rang=rang)
                print(my_salon.add(avto))
                logging.info("Mashina qo'shildi")

            elif tanlov == '2':
                zaryad_km = input("Zaryad (km): ")
                if rang == "":
                    elektro = ElektroAvto(zaryad_km, model, narx)
                else:
                    elektro = ElektroAvto(zaryad_km, model, narx, rang=rang)
                print(my_salon.add_e(elektro))

        elif tanlov == '3':
            for avto in my_salon:
                print(avto)

        elif tanlov == '4':
            try:
                raqam = int(input("Sotiladigan avto raqamini kiriting: "))
                ism = input("Mijozning ismi: ")
                tel = input("Mijozning telefoni: ")
                my_salon.sot(raqam, Mijoz(ism, tel))
            except ValueError:
                print("Iltimos, raqamni to'g'ri (son orqali) kiriting!")


        elif tanlov == '5':
            qimmat = my_salon.eng_qimmat()
            if qimmat:
                print(f"Eng qimmat avto: {qimmat}")
            else:
                print("Salonda sotuvda avto yo'q.")

        elif tanlov == "6":
            my_salon.saqla()

        elif tanlov == "7":
            my_salon.yukla()

        elif tanlov == '0':
            print("Dastur tugadi.")
            logging.info("Dastur tugatildi!")
            break

        else:
            print("Noto'g'ri tanlov. Qaytadan urinib ko'ring.")
            logging.warning("Noto'g'ri tanlov.")