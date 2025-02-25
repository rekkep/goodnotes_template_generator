import numpy as np

def perfect_fill(
    width: int, 
    height: int, 
    square_size: float,
    use_nearest_size: bool
    ):
    
    if width > height:
        new_width = int(height)
        new_height = int(width)
    else:
        new_width = int(width)
        new_height = int(height)
    
    # checks if the paper can be perfectly filled
    # with squares with squares of given side length
    if new_width % square_size == 0 and new_height % square_size == 0:
        return square_size
    else:
        # calculates common divisor
        common = np.array([])
        for d in range(1, int(min(new_width, new_height)) + 1):
            if int(new_width) % d == 0 and int(new_height) % d == 0:
                common = np.append(common, d)
        
        # returns the closest square size that will
        # fill the paper perfectly
        if use_nearest_size:
            square_size = min(common, key=lambda d: abs(d - square_size))
        else:
            print(f"not perfect size, perfect square size would be {min(common, key=lambda d: abs(d - square_size))}")
        return square_size