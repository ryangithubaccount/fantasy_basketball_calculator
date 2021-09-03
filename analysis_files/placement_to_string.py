def placement_to_string(num, data):
    for i in range(num):
        placement = int(data[i][3])
        if placement >= 0:
            if placement == 0:
                placement = "~0"
            else:
                placement = "+" + str(placement)
        else:
            placement = str(placement)
        data[i][3] = placement