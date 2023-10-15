
from core.descriptors import Gate, Composite, ExposedPin, Not
from core.simulator import JIT
from dflipflop import DFlipFlop

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
nor = Gate(Gate.OR, negated=True)
xor_ = Gate(Gate.XOR)
and_ = Gate(Gate.AND)
not_ = Not()


class AllSwitchesPressed(Composite):
    def __init__(self):
        super().__init__()

        # Inputs
        self.add_child('switchA', ein)
        self.add_child('switchB', ein)
        self.add_child('switchC', ein)
        self.add_child('switchD', ein)
        self.add_child('switchE', ein)
        self.add_child('switchF', ein)
        self.add_child('switchG', ein)
        self.add_child('switchH', ein)
        self.add_child('switchI', ein)

        # Outputs
        self.add_child('allpressed', eout)

        # Gates
        self.add_child('IC1A', and_)
        self.add_child('IC1B', and_)
        self.add_child('IC1C', and_)
        self.add_child('IC1D', and_)
        self.add_child('IC2A', and_)
        self.add_child('IC2B', and_)
        self.add_child('IC2C', and_)
        self.add_child('IC2D', and_)

        # Connect
        self.connect('switchA', '', 'IC1A', 'in0')
        self.connect('switchB', '', 'IC1A', 'in1')

        self.connect('switchC', '', 'IC1B', 'in0')
        self.connect('switchD', '', 'IC1B', 'in1')

        self.connect('switchE', '', 'IC1C', 'in0')
        self.connect('switchF', '', 'IC1C', 'in1')

        self.connect('switchG', '', 'IC1D', 'in0')
        self.connect('switchH', '', 'IC1D', 'in1')

        self.connect('IC1A', 'out', 'IC2A', 'in0')
        self.connect('IC1B', 'out', 'IC2A', 'in1')

        self.connect('IC1C', 'out', 'IC2B', 'in0')
        self.connect('IC1D', 'out', 'IC2B', 'in1')

        self.connect('IC1C', 'out', 'IC2B', 'in0')
        self.connect('IC1D', 'out', 'IC2B', 'in1')

        self.connect('IC2A', 'out', 'IC2C', 'in0')
        self.connect('IC2B', 'out', 'IC2C', 'in1')

        self.connect('IC2C', 'out', 'IC2D', 'in0')
        self.connect('switchI', '', 'IC2D', 'in1')

        self.connect('IC2D', 'out', 'allpressed', '')


if __name__ == '__main__':
    all_press = AllSwitchesPressed()
    sim = JIT(all_press, burst_size=1000, map_pins=True)
    sim.step()
    print('all pressed:', sim.get_pin_state('/allpressed/pin'))

    sim.set_pin_state('/switchA/pin', 1)
    sim.step()
    print('all pressed:', sim.get_pin_state('/allpressed/pin'))

    sim.set_pin_state('/switchB/pin', 1)
    sim.set_pin_state('/switchI/pin', 1)
    sim.step()
    print('all pressed:', sim.get_pin_state('/allpressed/pin'))

    sim.set_pin_state('/switchC/pin', 1)
    sim.set_pin_state('/switchE/pin', 1)
    sim.step()
    print('all pressed:', sim.get_pin_state('/allpressed/pin'))

    sim.set_pin_state('/switchD/pin', 1)
    sim.set_pin_state('/switchF/pin', 1)
    sim.set_pin_state('/switchG/pin', 1)
    sim.set_pin_state('/switchH/pin', 1)
    sim.step()
    print('all pressed:', sim.get_pin_state('/allpressed/pin'))
    
