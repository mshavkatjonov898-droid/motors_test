import unittest
from ustudy_motors1 import Avto, ElektroAvto, Mijoz, Salon


class TestUstudyMotors(unittest.TestCase):

    def setUp(self):
        """Har bir testdan oldin yangi salon va obyektlar yaratib olamiz"""
        self.salon = Salon("Test Motors")
        self.mijoz = Mijoz("Ali", "+998901234567")
        self.avto1 = Avto("Cobalt", 12000, rang="oq")
        self.avto2 = Avto("Gentra", 15000, egasi=self.mijoz, rang="qora")
        self.elektro1 = ElektroAvto(450, "BYD Han", 35000, rang="kulrang")
        self.elektro2 = ElektroAvto(300, "Tesla Model 3", 40000, egasi=self.mijoz, rang="qizil")

    # 1-test: Oddiy Avto (sotuvda va egasi bor) uchun get_info() formati
    def test_avto_get_info(self):
        self.assertEqual(self.avto1.get_info(), "🚗 oq Cobalt - 12000$ (sotuvda)")
        self.assertEqual(self.avto2.get_info(), "🚗 qora Gentra - 15000$ (Egasi: Ali)")

    # 2-test: ElektroAvto (sotuvda va egasi bor) uchun get_info() formati
    def test_elektro_avto_get_info(self):
        self.assertEqual(self.elektro1.get_info(), "⚡ kulrang BYD Han - 35000$ | zaryad: 450 km (sotuvda)")
        self.assertEqual(self.elektro2.get_info(), "⚡ qizil Tesla Model 3 - 40000$ | zaryad: 300 km (Egasi: Ali)")

    # 3-test: Salon.add va Salon.add_e metodlarini tekshirish
    def test_salon_add(self):
        javob1 = self.salon.add(self.avto1)
        javob2 = self.salon.add_e(self.elektro1)

        self.assertEqual(len(self.salon), 2)
        self.assertEqual(javob1, "Salonga qo'shildi: oq Cobalt — 12000$ (sotuvda)")
        self.assertEqual(javob2, "Salonga qo'shildi: kulrang BYD Han — 35000$ | zaryad: 450 km (sotuvda)")

    # 4-test: Salon.search — qidirilayotgan avto topildi
    def test_search_topildi(self):
        self.salon.add(self.avto1)
        self.salon.add_e(self.elektro1)
        natija = self.salon.search("Cobalt")
        self.assertEqual(len(natija), 1)
        self.assertEqual(natija[0].model, "Cobalt")

    # 5-test: Salon.search — qidirilayotgan avto topilmadi
    def test_search_topilmadi(self):
        self.salon.add(self.avto1)
        natija = self.salon.search("Malibu")
        self.assertEqual(len(natija), 0)

    # 6-test: Salon.search — katta-kichik harflarga sezgir emasligi (case-insensitive)
    def test_search_katta_kichik_harf(self):
        self.salon.add_e(self.elektro1)
        natija_kichik = self.salon.search("byd han")
        natija_katta = self.salon.search("BYD HAN")
        self.assertEqual(len(natija_kichik), 1)
        self.assertEqual(len(natija_katta), 1)

    # 7-test: Avto.jami_yaratilgan() va len(salon) hisoblagichlari
    def test_jami_yaratilgan(self):
        boshlangich_jami = Avto.jami_yaratilgan()
        yangi_avto = Avto("Onix", 16000)
        yangi_elektro = ElektroAvto(500, "Zeekr 001", 55000)
        self.assertEqual(Avto.jami_yaratilgan(), boshlangich_jami + 2)

    # 8-test: Sotuvdagi avtolarni filtrlash (sotuvda metodi)
    def test_sotuvda(self):
        self.salon.add(self.avto1)  # sotuvda
        self.salon.add(self.avto2)  # sotilgan (egasi Ali)
        self.salon.add_e(self.elektro1)  # sotuvda

        sotuvdagilar = self.salon.sotuvda()
        self.assertEqual(len(sotuvdagilar), 2)
        self.assertIn(self.avto1, sotuvdagilar)
        self.assertNotIn(self.avto2, sotuvdagilar)

    # 9-test: Eng qimmat avtoni aniqlash (__gt__ va eng_qimmat metodi)
    def test_eng_qimmat(self):
        self.salon.add(self.avto1)  # 12000$ (sotuvda)
        self.salon.add_e(self.elektro1)  # 35000$ (sotuvda)
        self.salon.add_e(self.elektro2)  # 40000$ (egasi bor, sotuvda emas!)

        self.assertEqual(self.salon.eng_qimmat(), self.elektro1)

    # 10-test: Avtomobilni sotish (sot metodi)
    def test_sotish(self):
        self.salon.add(self.avto1)
        yangi_mijoz = Mijoz("Vali", "+998991112233")
        self.salon.sot(1, yangi_mijoz)

        self.assertEqual(self.avto1.egasi, yangi_mijoz)
        self.assertEqual(len(self.salon.sotuvda()), 0)


if __name__ == "__main__":
    unittest.main()