from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    
    [ix, iy] = image_size
    [tx, ty] = tile_size
    
    if not ix % tx == 0 or not iy % ty == 0:
        return False
    
    region_count = (ix / tx) * (iy / ty)
    l = len(ordering)
    return len(set(ordering)) == l and l == region_count
            


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    
    img = Image.open(image_path, mode='r')
    
    [iw, ih] = img.size
    [tw, th] = tile_size
  
    if not valid_input((iw, ih), tile_size, ordering):
        img.close()
        raise ValueError("The tile size or ordering are not valid for the given image")
        
    # Split the image, join it, write it to out_path
    
    regions = []
    
    # dimensions may not be symmetrical
    #  len / r_len = row_count
    #  wid / r_wid = col_count
    # list size = r * c
    
    rc = ih // th
    cc = iw // tw

    # ordering is left to right, top to bottom
    # ! Not move left to right and top to bottom !
    for r in range(rc):
        sy = r * th
        for c in range(cc):
            sx = c * tw
            box = (sx, sy, sx + tw, sy + th)
            r = img.crop(box)
            regions.append(r)
    
    # for c in range(cc):
    #     for r in range(rc):
    #         sx = c * tw
    #         sy = r * th
    #         box = (sx, sy, sx + tw, sy + th)
    #         r = img.crop(box)
    #         regions.append(r)
    
    # Reorder the images in regions according to the ordering
    
    sorted_regions = []
    
    for index in ordering:
        r = regions[index]
        sorted_regions.append(r)
        # regions[index].close()
        regions[index] = None
    
    #? there is another way to do this maybe thats better cause that would involve skipping certain regions
    
    regions_counter = 0 # region counter # ? We may not need this `regions_counter` variable
    for r in range(rc):
        sy = r * th
        for c in range(cc):
            sx = c * tw
            box = (sx, sy, sx + tw, sy + th)
            img.paste(sorted_regions[regions_counter], box)
            regions_counter += 1

    # img.show()
    img.save(out_path)
    img.close()
