from time import sleep


def sayac(zaman):
    while zaman > 0:
        sleep(1)
        zaman -= 1
zaman=1
sayac(zaman)