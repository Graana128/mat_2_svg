import svgwrite


text = "asdfdsa"
font_size = 5

# Estimate text dimensions
text_width, text_height = 17, font_size
print(len(text), font_size, text_width)


# Create an SVG drawing
dwg = svgwrite.Drawing('example.svg', profile='tiny')

# Draw a rectangle around the text
rect = dwg.rect(insert=(10, 10), size=(text_width, text_height),
                fill='none', stroke='black')

# Add the rectangle to the drawing
dwg.add(rect)

# Add the text to the drawing
dwg.add(dwg.text(text, insert=(10, 10 + text_height - font_size * 0.2),
                 font_size=font_size, font_family='Helvetica'))

# Save the drawing
dwg.save()
