from image_processing.utils import find_images
import requests



def main():
    images = find_images()
    for image in images:
        response = requests.post(
            'http://localhost:8000/process',
            json = {
                "dryerId": 1,
                "dryerBaseSize": "1395x2757",
                "imageBase64": image,
                "itemsToProcess": [
                    {
                        "id": 1,
                        "cut_config": {"xx": 1090, "xy": 1100, "yx": 900, "yy": 910},
                        "name": "Chave ArFrio",
                        "type": {"name": "Chave", "id": 1}
                    },
                    # {
                    #     "id": 2,
                    #     "cut_config": {"xx": 570, "xy": 790, "yx": 1570, "yy": 1950},
                    #     "name": "Chave Temp",
                    #     "type": { "name": "Chave", "id": 1 }
                    # },
                    # {
                    #     "id": 3,
                    #     "cut_config": {"xx": 580, "xy": 780, "yx": 1950, "yy": 2310},
                    #     "name": "Chave On/Off",
                    #     "type": {"name": "Chave", "id": 1}
                    # },
                    # {
                    #     "id": 4,
                    #     "cut_config": {"xx": 530, "xy": 600, "yx": 1400, "yy": 1500},
                    #     "name": "Solda 1",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 5,
                    #     "cut_config": {"xx": 760, "xy": 860, "yx": 1390, "yy": 1530},
                    #     "name": "Solda 2",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 6,
                    #     "cut_config": {"xx": 630, "xy": 750, "yx": 1600, "yy": 1710},
                    #     "name": "Solda 3",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 7,
                    #     "cut_config": {"xx": 600, "xy": 685, "yx": 1810, "yy": 1935},
                    #     "name": "Solda 4",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 8,
                    #     "cut_config": {"xx": 700, "xy": 785, "yx": 1810, "yy": 1935},
                    #     "name": "Solda 5",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 9,
                    #     "cut_config": {"xx": 610, "xy": 710, "yx": 1980, "yy": 2060},
                    #     "name": "Solda 6",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 10,
                    #     "cut_config": {"xx": 570, "xy": 665, "yx": 2190, "yy": 2300},
                    #     "name": "Solda 7",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 11,
                    #     "cut_config": {"xx": 695, "xy": 770, "yx": 2190, "yy": 2300},
                    #     "name": "Solda 8",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 12,
                    #     "cut_config": {"xx": 530, "xy": 840, "yx": 2390, "yy": 2530},
                    #     "name": "Presilha",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 13,
                    #     "cut_config": {"xx": 560, "xy": 815, "yx": 2550, "yy": 2720},
                    #     "name": "Luva do Cabo",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 14,
                    #     "cut_config": {"xx": 90, "xy": 210, "yx": 540, "yy": 705},
                    #     "name": "Parafuso Esquerdo do Motor",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 15,
                    #     "cut_config": {"xx": 1080, "xy": 1220, "yx": 500, "yy": 660},
                    #     "name": "Parafuso Direito do Motor",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 16,
                    #     "cut_config": {"xx": 140, "xy": 1130, "yx": 20, "yy": 1080},
                    #     "name": "Motor",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                    # {
                    #     "id": 17,
                    #     "cut_config": {"xx": 890, "xy": 1080, "yx": 900, "yy": 1040},
                    #     "name": "Haste de Resistência",
                    #     "type": {"name": "Solda", "id": 1}
                    # },
                ],
            }
        )

        resp = response.json()
        print('yes')


if __name__ == '__main__':
    main()