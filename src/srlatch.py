from core.descriptors import Constant, Gate, Composite, ExposedPin, Not
from core.simulator import JIT

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
nor = Gate(Gate.OR, negated=True)
xor_ = Gate(Gate.XOR)
and_ = Gate(Gate.AND)
or_ = Gate(Gate.OR)
not_ = Not()
c = Constant(1, 0)


class SRLatch(Composite):
    def __init__(self):
        super().__init__()
        self.add_child('nor1', nor)
        self.add_child('s', ein)
        self.add_child('nor2', nor)
        self.add_child('r', ein)
        self.add_child('q', eout)
        self.add_child('q_', eout)

        self.connect('nor2', 'out', 'nor1', 'in1')
        self.connect('nor1', 'out', 'nor2', 'in0')
        self.connect('s', '', 'nor2', 'in1')
        self.connect('r', '', 'nor1', 'in0')
        self.connect('nor1', 'out', 'q', '')
        self.connect('nor2', 'out', 'q_', '')


if __name__ == '__main__':
    srlatch = SRLatch()

    # Initialize the JIT simulator with your srlatch
    sim = JIT(srlatch, burst_size=1000, map_pins=True)

    # Set initial states (example: setting 's' to 1 and 'r' to 0)
    sim.set_pin_state('/s/pin', 1)
    sim.set_pin_state('/r/pin', 0)

    # Run the simulator for a single step
    sim.step()

    # Observe the outputs
    q_state = sim.get_pin_state('/q/pin')
    print(f"Q: {q_state}")

    # Set initial states (example: setting 's' to 1 and 'r' to 0)
    sim.set_pin_state('/s/pin', 0)
    sim.set_pin_state('/r/pin', 1)

    # Run the simulator for a single step
    sim.step()

    # Observe the outputs
    q_state = sim.get_pin_state('/q/pin')
    print(f"Q: {q_state}")

    # Set initial states (example: setting 's' to 1 and 'r' to 0)
    sim.set_pin_state('/s/pin', 1)
    sim.set_pin_state('/r/pin', 0)

    # Run the simulator for a single step
    sim.step()

    # Observe the outputs
    q_state = sim.get_pin_state('/q/pin')
    print(f"Q: {q_state}")

    # Note: For the SR latch, make sure not to set 's' and 'r' both to 1 simultaneously,
    # as that's an undefined state.
