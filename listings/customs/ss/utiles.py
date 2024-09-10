import re


class Utiles:
    def __init__(self):
        pass

    def getToiletId(self, typeId):
        data = {
            "Toilet418": "1",
            "Toilet419": "2",
            "Toilet420": "3",
            "Toilet421": "4",
            "Toilet422": "5+",
            "Toilet423": "არ აქვს",
        }
        key_for_value = next((key for key, value in data.items() if value == typeId), None)
        if key_for_value is None:
            return False  # Or return a default value, such as 0
        return int(re.sub(r'\D', '', key_for_value))

    def getProjectId(self, typeId):
        data = {
            "ProjectType17": "ლენინგრადის",
            "ProjectType18": "ლვოვის",
            "ProjectType19": "კიევი",
            "ProjectType20": "თბილისური ეზო",
            "ProjectType25": "მოსკოვის",
            "ProjectType26": "ქალაქური",
            "ProjectType27": "ჩეხური",
            "ProjectType28": "ხრუშჩოვის",
            "ProjectType29": "თუხარელის",
            "ProjectType30": "ვეძისი",
            "ProjectType36": "იუგოსლავიის",
            "ProjectType38": "მეტრომშენის",
            "ProjectType4": "არასტანდარტული",
            "ProjectType5": "ყავლაშვილის",
        }
        key_for_value = next((key for key, value in data.items() if value == typeId), None)
        if key_for_value is None:
            return False
        return int(re.sub(r'\D', '', key_for_value))

    def getStateId(self, typeId):
        data = {
            "RealEstateState10": "სარემონტო",
            "RealEstateState11": "მიმდინარე რემონტი",
            "RealEstateState12": "ძველი რემონტით",
            "RealEstateState15": "გარემონტებული",
            "RealEstateState16": "ახალი რემონტით",
            "RealEstateState35": "მწვანე კარკასი",
            "RealEstateState8": "შავი კარკასი",
            "RealEstateState9": "თეთრი კარკასი",
        }
        key_for_value = next((key for key, value in data.items() if value == typeId), None)
        if key_for_value is None:
            return False
        return int(re.sub(r'\D', '', key_for_value))

    def getLivesWithId(self, typeId):
        data ={
            33: "მეპატრონე",
            32: "დამგირავებელი"
        }
        key_for_value = next((key for key, value in data.items() if value == typeId), None)
        if key_for_value is None:
            return False
        return key_for_value

    def getFloorId(self, typeId):
        data = {
            "FloorType409": "დუპლექსი",
            "FloorType410": "ტრიპლექსი",
            "FloorType411": "სხვენი"
        }
        key_for_value = next((key for key, value in data.items() if value == typeId), None)
        if key_for_value is None:
            return False
        return int(re.sub(r'\D', '', key_for_value))

    def getBallId(self, typeId):
        data = {
            "Balcony_Loggia412": "1",
            "Balcony_Loggia413": "2",
            "Balcony_Loggia414": "3",
            "Balcony_Loggia415": "4",
            "Balcony_Loggia416": "5",
            "Balcony_Loggia417": "არ აქვს",
        }
        key_for_value = next((key for key, value in data.items() if value == typeId), None)
        if key_for_value is None:
            return 417
        return int(re.sub(r'\D', '', key_for_value))

    def transform_number(self, num):
        return {"id":417,"has":False} if num == 0 else {"id":411 + num,"has":True}

ut = Utiles()

