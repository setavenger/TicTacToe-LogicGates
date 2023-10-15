from core.descriptors import Constant, Gate, Composite, ExposedPin, Not
from core.simulator import JIT
from dflipflop import DFlipFlop

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
nor = Gate(Gate.OR, negated=True)
xor_ = Gate(Gate.XOR)
and_ = Gate(Gate.AND)
or_ = Gate(Gate.OR)
not_ = Not()
c = Constant(1, 0)


class OneWinner(Composite):
    def __init__(self):
        super().__init__()
        # inputs
        self.add_child('pla1win', ein)
        self.add_child('pla2win', ein)

        # outputs
        self.add_child('pla1win_indicator', eout)
        self.add_child('pla2win_indicator', eout)

        # components
        self.add_child('IC1A', DFlipFlop())
        self.add_child('IC1B', DFlipFlop())

        # connect
        self.connect('pla1win', '', 'IC1A', 'clk')
        self.connect('pla2win', '', 'IC1B', 'clk')
        self.connect('IC1A', 'q_', 'IC1B', 'd')
        self.connect('IC1B', 'q_', 'IC1A', 'd')

        self.connect('IC1A', 'q', 'pla1win_indicator', '')
        self.connect('IC1B', 'q', 'pla2win_indicator', '')


if __name__ == '__main__':
    one_win = OneWinner()
    sim = JIT(one_win, burst_size=1000, map_pins=True)


    def read_vals():
        print('/pla1win_indicator/pin:', sim.get_pin_state('/pla1win_indicator/pin'))
        print('/pla2win_indicator/pin:', sim.get_pin_state('/pla2win_indicator/pin'))


    sim.step()
    read_vals()

    sim.set_pin_state('/pla1win/pin', 1)
    sim.step()
    read_vals()

    sim.set_pin_state('/pla2win/pin', 1)
    sim.step()
    read_vals()
