from plantuml import PlantUML

PLANT_UML = PlantUML(url = "http://www.plantuml.com/plantuml/png/")

def plantuml_to_image(code: str, output_file: str):
    with open(output_file, "wb") as img_file:
        img_file.write(PLANT_UML.processes(code))

