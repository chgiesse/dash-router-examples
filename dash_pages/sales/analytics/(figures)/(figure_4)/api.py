from time import sleep


def endpoint(*args, **kwargs):
    sleep(0.6)
    labels = ["Oxygen", "Hydrogen", "Carbon_Dioxide", "Nitrogen"]
    values = [4500, 2500, 1053, 500]

    return labels, values
