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
                if texture.m_Name in textures:
                    if texture.image != textures[texture.m_Name]:
                        print('DUPLICATE:', texture.m_Name)
                        os.makedirs('output', exist_ok=True)
                        texture.image.save('output/{} (1).png'.format(texture.m_Name))
                        textures[texture.m_Name].save('output/{} (2).png'.format(texture.m_Name))
                textures[texture.m_Name] = texture.image
