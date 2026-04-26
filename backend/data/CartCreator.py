import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json


class CartCreator():
    def __init__(self):
        self.amount_of_blood = {1: 397, 2: 405, 3: 398}

        self.type_of_feeding = {"Бестия": 103,"Джентльмен": 111,"Идол": 101,"Искуситель": 93,"Морфей": 101,"Налётчик": 84,"Преследователь": 95,"Придорожный убийца": 106,"Расхититель могил": 97,"Семьянин": 104,"Суррогатчик": 95,"Фермер": 110}
        
        self.resununs= {"Меланхолический": 197,"Нет значения": 184,"Пусто": 211,"Сангвинистический": 155,"Флегматический": 239,"Холерический": 214}

        self.event = {"Тебе не повезло. На твой след напали Охотники.": 114,
                        "Тебе не повезло. Ты попал в засаду.": 4,
                        "В любом случае твой уровень здоровья по возвращению + 4(ухудшилось на 4, но не хуже 5-го), ты не можешь совершать попыток кормления в этот цикл больше.": 4,
                        "Во время охоты ты почувствовал странный холодок. Если ты владеешь Обливионом или иным образом можешь видеть духов - ты видел слабый силуэт. Попытка взаимодействия уменьшит полученный тобой обьем крови на единицу, но возможно ты получишь иное? Если хочешь - обратись к макроносферу.": 148,
                        "Во время твоей охоты произошло неприятно столкновение с чем-то огромным и мохнатым. Если ты применил стремительность - ты сбежал без эффектов (но и без крови). В другом случае если твой тип питания указан первым - ты получил весь обьем крови, иначе - половину, а так же +1 уровень здоровья (ухудшилось).": 111,
                        "Если решка - кормление не удалось в любом случае.": 114,
                        "Если твой резонанс совпал с резонансом карточки - ты насытился на еще один пункт больше.": 18,
                        "Кинь монетку - если орел, то ты получил с карточки кровь.": 114,
                        "Ничего не случилось": 587,
                        "Очень большая удача - ты обрел нож. Возьми у макроносфера.": 1,
                        "Твое здоровье получает один уровень повреждений.": 114,
                        "Ты видел странного человека, что наблюдал за тобой все время. Ты так и не понял смертный он или нет, догнать тебе его не удалось.": 110,
                        "Ты долго не мог выбрать подходящую жертву и ситуация никак не складывалась. Если твой тип питания первый на карточке - ты все равно достиг успеха. В остальных случаях - брось монетку за каждую единицу крови и забери те, которые были успехом.": 105,
                        "Ты нарвался на стаю из нескольких крупных мохнатых существ. Кинь монетку столько раз сколько крови полагается за эту карту - при победе ты получишь ее. Твой уровень здоровья по возвращению - 5, ты на грани торпора и ухудшение здоровья произойдет через пол часа если тебе не оказать помощь по правилам.": 2,
                        "Ты получил кровь с этой карты если твой резонанс совпадает с ее.": 4}

    
    def generator(self):

        rand_amount_of_blood = random.choices(
            population=list(self.amount_of_blood.keys()),
            weights=list(self.amount_of_blood.values()),
            k=1
        )[0]
        rand_type_of_feeding1 = random.choices(
            population=list(self.type_of_feeding.keys()),
            weights=list(self.type_of_feeding.values()),
            k=1
        )[0]
        
        rand_type_of_feeding2 = random.choices(
            population=list(self.type_of_feeding.keys()),
            weights=list(self.type_of_feeding.values()),
            k=1
        )[0]
        
        rand_type_of_feeding3 = random.choices(
            population=list(self.type_of_feeding.keys()),
            weights=list(self.type_of_feeding.values()),
            k=1
        )[0]
        rand_resonuns = random.choices(
            population=list(self.resununs.keys()),
            weights=list(self.resununs.values()),
            k=1
        )[0]
        rand_event = random.choices(
            population=list(self.event.keys()),
            weights=list(self.event.values()),
            k=1
        )[0]
        font = ImageFont.truetype("arial.ttf", 20)
        values = [rand_amount_of_blood,rand_type_of_feeding1,rand_type_of_feeding2,rand_type_of_feeding3,rand_resonuns,rand_event]    
        template_path = Path(__file__).with_name("default.jpg")
        with Image.open(template_path) as template:
            img = template.copy()
        draw = ImageDraw.Draw(img)

        draw.text((450, 260), str(values[0]), fill="white", font=font, anchor="mm", align="center")
        draw.text((450, 380), str(values[1]), fill="black", font=font, anchor="mm", align="center")
        draw.text((450, 510), str(values[2]), fill="black", font=font, anchor="mm", align="center")
        draw.text((450, 640), str(values[3]), fill="black", font=font, anchor="mm", align="center")
        draw.text((450, 770), str(values[4]), fill="black", font=font,anchor="mm", align="center")
        if len(str(values[5])) >= 40:
            draw.text((257, 880), str(values[5])[:40], fill="black", font=font)
            draw.text((257, 910), str(values[5])[40:80], fill="black", font=font)
            draw.text((257, 940), str(values[5])[80:120], fill="black", font=font)
            draw.text((257, 970), str(values[5])[120:160], fill="black", font=font)
        else:
            draw.text((257, 880), str(values[5]), fill="black", font=font)
    

        
        all_info = {"amount of blood":rand_amount_of_blood,
                    "feedind 1":rand_type_of_feeding1,
                    "feeding 2":rand_type_of_feeding2,
                    "feeding 3":rand_type_of_feeding3,
                    "resonuns":rand_resonuns,
                    "event":rand_event}



        return img,all_info

if __name__ == "__main__":
    creator = CartCreator()
    a = creator.generator()[0]
    preview_path = Path(__file__).with_name("cart_preview.jpg")
    a.save(preview_path)
    a.show()
    print(f"Preview saved to: {preview_path}")
    




    
    




