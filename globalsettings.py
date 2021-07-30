STANDARD_TICK_LENGTH = 0.001
STRIP_LENGTH = 144
STRIP_SEGMENTS = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36, 48, 72]
STRIP_SEGMENTS2 = [1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72]
STRIP_SEGMENTS2_EVEN = [2, 4, 6, 8, 12, 18, 24, 36, 72]
STRIP_SEGMENTS3 = [1, 2, 3, 4, 6, 8, 12, 16, 24, 48]
STRIP_SEGMENTS4 = [1, 2, 3, 4, 6, 9, 12, 18, 36]

#not used atm
def set_segments():
    STRIP_SEGMENTS = []
    
    for y in range(1, STRIP_LENGTH):
        if STRIP_LENGTH%y==0:
            STRIP_SEGMENTS.append(y)
            
    print(STRIP_SEGMENTS)
