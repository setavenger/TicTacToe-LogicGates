from core.descriptors import Gate, Composite, ExposedPin, Not
from core.simulator import JIT
from dflipflop import DFlipFlop

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
nor = Gate(Gate.OR, negated=True)
xor_ = Gate(Gate.XOR)
and_ = Gate(Gate.AND)
not_ = Not()


class SwitchInput(Composite):
    def __init__(self):
        super().__init__()

        # Inputs and Outputs
        self.add_child('switch_input', ein)
        self.add_child('pla1profile', ein)
        self.add_child('pla2profile', ein)

        self.add_child('pla1out', eout)
        self.add_child('pla2out', eout)
        self.add_child('switchout', eout)

        # Components
        self.add_child('dffmaster', DFlipFlop())
        self.add_child('dffpla1', DFlipFlop())
        self.add_child('dffpla2', DFlipFlop())
        self.add_child('xor1', xor_)
        self.add_child('and1', and_)
        self.add_child('not1', not_)

        # Master connections
        self.connect('switch_input', '', 'dffmaster', 'clk')
        self.connect('switch_input', '', 'dffmaster', 'd')

        # Logic to create a controlled clock pulse
        self.connect('dffmaster', 'q', 'and1', 'in0')
        self.connect('xor1', 'out', 'not1', 'in')
        self.connect('not1', 'out', 'and1', 'in1')

        # Player 1's flip-flop connections
        self.connect('and1', 'out', 'dffpla1', 'clk')
        self.connect('pla1profile', '', 'dffpla1', 'd')

        # Player 2's flip-flop connections
        self.connect('and1', 'out', 'dffpla2', 'clk')
        self.connect('pla2profile', '', 'dffpla2', 'd')

        # Outputs and XOR logic
        self.connect('dffpla1', 'q', 'pla1out', '')
        self.connect('dffpla1', 'q', 'xor1', 'in0')
        self.connect('dffpla2', 'q', 'pla2out', '')
        self.connect('dffpla2', 'q', 'xor1', 'in1')
        self.connect('xor1', 'out', 'switchout', '')


if __name__ == '__main__':
    sw_in = SwitchInput()
    sim = JIT(sw_in, burst_size=1000, map_pins=True)


    def read_vals():
        print(''.join(['-' for _ in range(25)]))
        print('clocks:')
        print('/dffpla1/clk/pin:', sim.get_pin_state('/dffpla1/clk/pin'))
        print('/dffpla2/clk/pin:', sim.get_pin_state('/dffpla2/clk/pin'))
        print('data:')
        print('/dffpla1/d/pin:', sim.get_pin_state('/dffpla1/d/pin'))
        print('/dffpla2/d/pin:', sim.get_pin_state('/dffpla2/d/pin'))
        print('outputs:')
        print('/pla1out/pin:', sim.get_pin_state('/pla1out/pin'))
        print('/pla2out/pin:', sim.get_pin_state('/pla2out/pin'))
        print('/switchout/pin:', sim.get_pin_state('/switchout/pin'))
        print('/xor1/out:', sim.get_pin_state('/xor1/out'))


    sim.step()
    read_vals()

    sim.set_pin_state('/pla1profile/pin', 1)
    sim.set_pin_state('/switch_input/pin', 1)

    # needs to steps to ensure that the recursive signal from xor1 settles
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/pla1profile/pin', 0)
    sim.set_pin_state('/pla2profile/pin', 1)
    sim.set_pin_state('/switch_input/pin', 1)

    # needs to steps to ensure that the recursive signal from xor1 settles
    sim.step()
    sim.step()
    read_vals()
