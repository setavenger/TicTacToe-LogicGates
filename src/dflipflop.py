from core.descriptors import Gate, Composite, ExposedPin, Not
from core.simulator import JIT
from srlatch import SRLatch

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
nor = Gate(Gate.OR, negated=True)
xor_ = Gate(Gate.XOR)
and_ = Gate(Gate.AND)
not_ = Not()


class DFlipFlop(Composite):
    def __init__(self):
        super().__init__()

        # Inputs
        self.add_child('d', ein)
        self.add_child('clk', ein)
        self.add_child('set', ein)
        self.add_child('reset', ein)

        # Outputs
        self.add_child('q', eout)
        self.add_child('q_', eout)

        # Internal Components
        self.add_child('sr', SRLatch())
        self.add_child('and1', and_)
        self.add_child('and2', and_)
        self.add_child('not_d', not_)

        # Connect
        self.connect('and1', 'out', 'sr', 's')
        self.connect('and2', 'out', 'sr', 'r')
        self.connect('d', '', 'and1', 'in0')
        self.connect('d', '', 'not_d', 'in')
        self.connect('not_d', 'out', 'and2', 'in0')
        self.connect('clk', '', 'and1', 'in1')
        self.connect('clk', '', 'and2', 'in1')
        self.connect('set', '', 'sr', 's')
        self.connect('reset', '', 'sr', 'r')
        self.connect('sr', 'q', 'q', '')
        self.connect('sr', 'q_', 'q_', '')


if __name__ == '__main__':
    ff = DFlipFlop()
    sim = JIT(ff, burst_size=1000, map_pins=True)

    sim.step()

    out = sim.get_pin_state('/q/pin')
    print(out)

    sim.set_pin_state('/clk/pin', 1)
    sim.step()
    out = sim.get_pin_state('/q/pin')
    print(out)

    # sim.set_pin_state('/clk/pin', 1)
    sim.set_pin_state('/d/pin', 1)
    sim.step()
    out = sim.get_pin_state('/q/pin')
    print(out)
