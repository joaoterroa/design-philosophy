from pathlib import Path
from PIL import Image, ImageDraw
folder=Path(__file__).resolve().parent/'screenshots'
for theme in ['light','dark']:
    sheet=Image.new('RGB',(1400,720),(213,218,215))
    draw=ImageDraw.Draw(sheet)
    for i,state in enumerate(['main','compose','review','pending','offline','empty','accepted']):
        img=Image.open(folder/f'{state}-{theme}.png').resize((200,340))
        x=(i%4)*350+70;y=(i//4)*360+20
        sheet.paste(img,(x,y))
        draw.text((x,y-15),state,fill=(25,35,25))
    sheet.save(folder/f'contact-{theme}.png')
