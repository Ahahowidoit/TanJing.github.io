"""
        此代码用于调整图片大小
"""
import pygame
def resize_bmp_image(input_file, output_file, new_width, new_height):
    # 加载图像
    image = pygame.image.load(input_file)

    # 调整尺寸
    new_size = (new_width, new_height)
    scaled_image = pygame.transform.scale(image, new_size)

    # 保存图像
    pygame.image.save(scaled_image, output_file)

# 调用函数并指定参数
resize_bmp_image('images/ship.bmp', 'new_image.bmp', 50, 50)

