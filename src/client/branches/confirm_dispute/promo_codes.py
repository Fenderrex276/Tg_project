from db.models import BlogerPromocodes


def load_promo_codes_blogers():
    arr = ['d37904b970', '342447934a', 'e9f2f8b2cb', '02e79a265a', 'a1bd18deab', '7d0dd7962e', 'a642d87245',
           '372f2f523a',
           '355d4f98d0', 'bd65eaa9fb', 'bed79a8378', '4554ac4d83', '5d3d2ebd43', '91218eda05', '6f6cb22df3',
           '357c1c9a8e',
           'e36c62fd57', 'f5ff667a12', 'e2ba4ff0c0', '629198bb9d', '57001a9f12', '83725b2923', '0bee8b8aeb',
           'c33d5f250a',
           '62b5c16c7f', 'e63b2478dd', '201398dbbd', 'f3c7ba67dc', '383e1129f2', 'e7a983b444', 'c6e639d99d',
           '66c0d468d6',
           'a3ae095e4f', 'ae0764f3d0', 'eb255784bf', 'd2e2d6ad6c', '701359690a', '14a5bd6e9f', '920c6e4fb1',
           '98803010da',
           '1c3feb00f3', '5436a89b1f', '6bab9a3434', '1a7c0f0de3', '5466e13458', '1c923e21b8', '9fd633b17a',
           '98b1a85923',
           '6fd5ea0420', 'b3c3da23cf', '46cf1b3633', 'b886884188', '49046e2f88', 'a11527789c', 'dcb9b2aa9d',
           '6728e1ddda',
           'e19b175b16', 'ff69697d2a', '5af6a5d5a6', 'ddde27c52d', 'fb2a128b96', 'bc846da924', '8fd1fb7d3f',
           '5121408cdb',
           '06c9774d6e', '3ca479c1e6', '25071a116d', '9d14acda50', 'a0816684eb', 'b11fc856cd', '08f2695866',
           '0065afb45e',
           '364b9f25d9', '414419a97f', '24ea0e61ed', '9e63c700c8', 'a34f5322aa', 'f603139b50', 'd0ffcbb545',
           'fdcef5cb63',
           '918f003b3d', 'ea09ffb370', '1f861c82f5', '16174ac8de', '6bbc714547', 'ee311f61c2', '3927609fb6',
           'ba97b22394',
           '3ffde1b4c7', 'acec7829bc', 'c1304fb8f2', 'daee3a98ba', '3b63f65a9b', '028d21ec52', '0f7c800306',
           '8399f2b50f',
           '57c2a95c5f', '40098515da', '4d7098fe05', '9c9af205d9']

    for el in arr:
        BlogerPromocodes.objects.create(promocode=el)

