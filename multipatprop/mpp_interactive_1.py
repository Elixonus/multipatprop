try:
    from math import pi
    from random import seed, random, randint
    from multipatprop import System, Transmitter, Receiver, Interferer, Point
    from output import render

    seed(1123)

    print(
        "This interactive example will simulate the multipath propagation of waves around a city environment."
    )

    receiver_x = 0.0
    receiver_y = 0.0

    while True:
        try:
            print(
                "\n(-5, -5) is the bottom left of the viewport, (5, 5) is the top right of the viewport."
            )
            print("The transmitter is hardcoded positioned at (-2, -2.5).")
            print("Enter the position of the receiver.")
            receiver_x = float(input("Receiver x: "))
            receiver_y = float(input("Receiver y: "))
        except Exception as e:
            if e is not KeyboardInterrupt:
                continue
            else:
                exit()
        break
    print(f"Receiver position is successfully set to ({receiver_x}, {receiver_y})\n")

    transmitter = Transmitter(Point(-2, -2.5))
    receiver = Receiver(Point(receiver_x, receiver_y))
    interferers = [Interferer.square(Point(0, 0), 9, 0)]


    for x in range(8):
        for y in range(8):
            interferer = Interferer.rectangle(
                position=Point(x - 3.5 + random() / 4, y - 3.5 + random() / 4),
                length=0.3 + random() / 4,
                width=0.25,
                rotation=pi / 2 * randint(0, 100),
            )
            interferers.append(interferer)


    system = System(transmitter, receiver, interferers)
    multipath = system.get_multipath(
        starting_number=1000,
        receiver_diameter=0.2,
        max_reflections=40,
        power_multiplier=0.9,
    )
    camera_position = Point(0, 0)
    camera_zoom = 0.1
    render(
        system, multipath, camera_position, camera_zoom, ui_size=1, bins=30, red_factor=1
    )
except KeyboardInterrupt:
    exit()
