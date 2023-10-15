from core.descriptors import Gate, Composite, ExposedPin, Not
from core.simulator import JIT

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
xor_ = Gate(Gate.XOR)
not_ = Not()


class ProfileGenerator(Composite):
    def __init__(self):
        super().__init__()

        # Inputs
        self.add_child('fieldA', ein)
        self.add_child('fieldB', ein)
        self.add_child('fieldC', ein)
        self.add_child('fieldD', ein)
        self.add_child('fieldE', ein)
        self.add_child('fieldF', ein)
        self.add_child('fieldG', ein)
        self.add_child('fieldH', ein)
        self.add_child('fieldI', ein)

        # Outputs
        self.add_child('profile1', eout)
        self.add_child('profile2', eout)

        # Inverter
        self.add_child('not1', not_)

        # Adding XOR gates
        self.add_child('IC1A', xor_)
        self.add_child('IC1B', xor_)
        self.add_child('IC1C', xor_)
        self.add_child('IC1D', xor_)
        self.add_child('IC2A', xor_)
        self.add_child('IC2B', xor_)
        self.add_child('IC2C', xor_)
        self.add_child('IC2D', xor_)

        # Connecting XOR gates
        self.connect('IC1A', 'out', 'IC2A', 'in0')
        self.connect('IC1B', 'out', 'IC2A', 'in1')

        self.connect('IC1C', 'out', 'IC2B', 'in0')
        self.connect('IC1D', 'out', 'IC2B', 'in1')

        self.connect('IC2A', 'out', 'IC2C', 'in0')
        self.connect('IC2B', 'out', 'IC2C', 'in1')

        self.connect('IC2C', 'out', 'IC2D', 'in0')

        # field inputs
        self.connect('fieldA', '', 'IC1A', 'in0')
        self.connect('fieldB', '', 'IC1A', 'in1')

        self.connect('fieldC', '', 'IC1B', 'in0')
        self.connect('fieldD', '', 'IC1B', 'in1')

        self.connect('fieldE', '', 'IC1C', 'in0')
        self.connect('fieldF', '', 'IC1C', 'in1')

        self.connect('fieldG', '', 'IC1D', 'in0')
        self.connect('fieldH', '', 'IC1D', 'in1')

        self.connect('fieldI', '', 'IC2D', 'in1')

        # profiles
        self.connect('IC2D', 'out', 'profile2', '')

        # player 1 is inverted
        self.connect('IC2D', 'out', 'not1', 'in')
        self.connect('not1', 'out', 'profile1', '')


if __name__ == '__main__':
    profile_generator = ProfileGenerator()
    sim = JIT(profile_generator, burst_size=1000, map_pins=True)

    sim.step()

    p1 = sim.get_pin_state('/profile1/pin')
    p2 = sim.get_pin_state('/profile2/pin')

    print(f"Turn: {p1}-{p2}")

    sim.set_pin_state('/fieldA/pin', 1)

    sim.step()

    p1 = sim.get_pin_state('/profile1/pin')
    p2 = sim.get_pin_state('/profile2/pin')

    print(f"Turn: {p1}-{p2}")

    sim.set_pin_state('/fieldG/pin', 1)

    sim.step()

    p1 = sim.get_pin_state('/profile1/pin')
    p2 = sim.get_pin_state('/profile2/pin')

    print(f"Turn: {p1}-{p2}")

    sim.set_pin_state('/fieldC/pin', 1)

    sim.step()

    p1 = sim.get_pin_state('/profile1/pin')
    p2 = sim.get_pin_state('/profile2/pin')

    print(f"Turn: {p1}-{p2}")

    sim.set_pin_state('/fieldB/pin', 1)

    sim.step()

    p1 = sim.get_pin_state('/profile1/pin')
    p2 = sim.get_pin_state('/profile2/pin')

    print(f"Turn: {p1}-{p2}")
