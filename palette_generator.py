import colorgram
import requests


class PaletteGenerator:
    def __init__(self, image_name, image_url, num_colors):
        self.image_name = image_name
        self.image_url = image_url
        self.num_colors = num_colors
        self.save_image()
        
    def save_image(self):
        response = requests.get(self.image_url)
        with open(f"static/images/{self.image_name}.jpg", "wb") as file:
            file.write(response.content)

    def generate_palette(self):
        colors = colorgram.extract(f"static/images/{self.image_name}.jpg", self.num_colors)
        colors.sort(key=lambda c: c.rgb.r, reverse=True)
        return [f"{color.rgb.r, color.rgb.g, color.rgb.b}" for color in colors]
        