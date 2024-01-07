"""
Goals:
    - Find recipe options
        - bool Alternates
    - Production
    - Favorites
"""


def main():
    menu = Interface()
    while True:
        menu.update()
        menu.loop()

if __name__ == '__main__': main()
