from core.descriptors import Gate, Composite, ExposedPin
from core.simulator import JIT

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
or_ = Gate(Gate.OR)
and3_ = Gate(Gate.AND, num_inputs=3)


class WinningDetector(Composite):
    def __init__(self):
        super().__init__()

        # Inputs
        self.add_child('A', ein)
        self.add_child('B', ein)
        self.add_child('C', ein)
        self.add_child('D', ein)
        self.add_child('E', ein)
        self.add_child('F', ein)
        self.add_child('G', ein)
        self.add_child('H', ein)
        self.add_child('I', ein)

        # Outputs
        self.add_child('won', eout)

        # Adding AND gates
        self.add_child('IC1A', and3_)
        self.add_child('IC1B', and3_)
        self.add_child('IC1C', and3_)
        self.add_child('IC2A', and3_)
        self.add_child('IC2B', and3_)
        self.add_child('IC2C', and3_)
        self.add_child('IC3C', and3_)
        self.add_child('IC4C', and3_)

        # Adding OR gates
        self.add_child('IC5A', or_)
        self.add_child('IC5B', or_)
        self.add_child('IC5C', or_)
        self.add_child('IC5D', or_)

        self.add_child('IC6A', or_)
        self.add_child('IC6B', or_)
        self.add_child('IC6C', or_)

        # Connecting AND gates to OR gates
        self.connect('IC1A', 'out', 'IC5A', 'in0')
        self.connect('IC1B', 'out', 'IC5A', 'in1')

        self.connect('IC1C', 'out', 'IC5B', 'in0')
        self.connect('IC2A', 'out', 'IC5B', 'in1')

        self.connect('IC2B', 'out', 'IC5C', 'in0')
        self.connect('IC2C', 'out', 'IC5C', 'in1')

        self.connect('IC3C', 'out', 'IC5D', 'in0')
        self.connect('IC4C', 'out', 'IC5D', 'in1')

        # Connecting the 2-input OR gates to the 3-input OR gates
        self.connect('IC5A', 'out', 'IC6A', 'in0')
        self.connect('IC5B', 'out', 'IC6A', 'in1')

        self.connect('IC5C', 'out', 'IC6B', 'in0')
        self.connect('IC5D', 'out', 'IC6B', 'in1')

        # Connecting to the final OR gate
        self.connect('IC6A', 'out', 'IC6C', 'in0')
        self.connect('IC6B', 'out', 'IC6C', 'in1')

        # A B C
        # D E F
        # G H I

        # Connecting inputs to AND gates
        self.connect('A', '', 'IC1A', 'in0')
        self.connect('B', '', 'IC1A', 'in1')
        self.connect('C', '', 'IC1A', 'in2')

        self.connect('D', '', 'IC1B', 'in0')
        self.connect('E', '', 'IC1B', 'in1')
        self.connect('F', '', 'IC1B', 'in2')

        self.connect('G', '', 'IC1C', 'in0')
        self.connect('H', '', 'IC1C', 'in1')
        self.connect('I', '', 'IC1C', 'in2')

        self.connect('A', '', 'IC2A', 'in0')
        self.connect('D', '', 'IC2A', 'in1')
        self.connect('G', '', 'IC2A', 'in2')

        self.connect('B', '', 'IC2B', 'in0')
        self.connect('E', '', 'IC2B', 'in1')
        self.connect('H', '', 'IC2B', 'in2')

        self.connect('C', '', 'IC2C', 'in0')
        self.connect('F', '', 'IC2C', 'in1')
        self.connect('I', '', 'IC2C', 'in2')

        self.connect('A', '', 'IC3C', 'in0')
        self.connect('E', '', 'IC3C', 'in1')
        self.connect('I', '', 'IC3C', 'in2')

        self.connect('C', '', 'IC4C', 'in0')
        self.connect('E', '', 'IC4C', 'in1')
        self.connect('G', '', 'IC4C', 'in2')

        # connect winning output
        self.connect('IC6C', 'out', 'won', '')


if __name__ == '__main__':
    win_detector = WinningDetector()
    sim = JIT(win_detector, burst_size=1000, map_pins=True)

    sim.set_pin_state('/A/pin', 1)
    sim.set_pin_state('/B/pin', 1)
    sim.set_pin_state('/D/pin', 1)

    sim.step()

    won = sim.get_pin_state('/won/pin')
    print(f"Won: {won}")
