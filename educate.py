import os
import UnityPy

textures = {}

for dirname in os.listdir('input'):
    path = 'input/{}'.format(dirname)
    if os.path.isdir(path) and dirname.startswith('educate'):
        educate = UnityPy.load(path)
        for obj in educate.objects:
            if obj.type.name == 'Texture2D':
                texture = obj.read()
                if texture.name in textures:
                    if texture.image != textures[texture.name]:
                        print('DUPLICATE:', texture.name)
                        os.makedirs('output', exist_ok=True)
                        texture.image.save('output/{} (1).png'.format(texture.name))
                        textures[texture.name].save('output/{} (2).png'.format(texture.name))
                textures[texture.name] = texture.image
