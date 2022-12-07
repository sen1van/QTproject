def collide_2_rect(rect1xy=[0, 0], rect1wh=[0, 0], rect2xy=[0, 0], rect2wh=[0, 0]):
    if rect1xy[0] + rect1wh[0] >= rect2xy[0]:
        if rect2xy[0] + rect2wh[0] >= rect1xy[0]:
            if rect1xy[1] + rect1wh[1] >= rect2xy[1]:
                if rect2xy[1] + rect2wh[1] >= rect1xy[1]:
                    return True
    return False

def collide_2_lines(line1p,line1w,line2p,line2w):
    if line1p + line1w >= line2p:
        if line2p + line2w >= line1p:
            return True
    return False