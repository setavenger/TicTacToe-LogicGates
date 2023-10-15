from core.descriptors import Constant, Gate, Composite, ExposedPin, Not
from core.simulator import JIT
from switchinput import SwitchInput
from profilegenerator import ProfileGenerator
from winningdetector import WinningDetector
from allswitchespressed import AllSwitchesPressed
from onewinner import OneWinner

ein = ExposedPin(ExposedPin.IN)
eout = ExposedPin(ExposedPin.OUT)
nor = Gate(Gate.OR, negated=True)
xor_ = Gate(Gate.XOR)
and_ = Gate(Gate.AND)
or_ = Gate(Gate.OR)
not_ = Not()
c = Constant(1, 0)


class TicTacToe(Composite):
    def __init__(self):
        super().__init__()

        # inputs
        self.add_child('switchAin', ein)
        self.add_child('switchBin', ein)
        self.add_child('switchCin', ein)
        self.add_child('switchDin', ein)
        self.add_child('switchEin', ein)
        self.add_child('switchFin', ein)
        self.add_child('switchGin', ein)
        self.add_child('switchHin', ein)
        self.add_child('switchIin', ein)

        # self.add_child('reset', ein)

        # outputs
        self.add_child('pla1win_indicator', eout)
        self.add_child('pla2win_indicator', eout)
        self.add_child('all_pressed_out', eout)

        # switches
        self.add_child('switchA', SwitchInput())
        self.add_child('switchB', SwitchInput())
        self.add_child('switchC', SwitchInput())
        self.add_child('switchD', SwitchInput())
        self.add_child('switchE', SwitchInput())
        self.add_child('switchF', SwitchInput())
        self.add_child('switchG', SwitchInput())
        self.add_child('switchH', SwitchInput())
        self.add_child('switchI', SwitchInput())

        # profile
        self.add_child('profile_gen', ProfileGenerator())

        # win detector
        self.add_child('win_pla1', WinningDetector())
        self.add_child('win_pla2', WinningDetector())
        self.add_child('all_pressed', AllSwitchesPressed())
        self.add_child('one_win', OneWinner())

        # Connections
        # Switches
        self.connect('switchAin', '', 'switchA', 'switch_input')
        self.connect('switchBin', '', 'switchB', 'switch_input')
        self.connect('switchCin', '', 'switchC', 'switch_input')
        self.connect('switchDin', '', 'switchD', 'switch_input')
        self.connect('switchEin', '', 'switchE', 'switch_input')
        self.connect('switchFin', '', 'switchF', 'switch_input')
        self.connect('switchGin', '', 'switchG', 'switch_input')
        self.connect('switchHin', '', 'switchH', 'switch_input')
        self.connect('switchIin', '', 'switchI', 'switch_input')

        # self.connect('reset', '', 'switchA', 'reset')
        # self.connect('reset', '', 'switchB', 'reset')
        # self.connect('reset', '', 'switchC', 'reset')
        # self.connect('reset', '', 'switchD', 'reset')
        # self.connect('reset', '', 'switchE', 'reset')
        # self.connect('reset', '', 'switchF', 'reset')
        # self.connect('reset', '', 'switchG', 'reset')
        # self.connect('reset', '', 'switchH', 'reset')
        # self.connect('reset', '', 'switchI', 'reset')

        # Profile
        self.connect('switchA', 'switchout', 'profile_gen', 'fieldA')
        self.connect('switchB', 'switchout', 'profile_gen', 'fieldB')
        self.connect('switchC', 'switchout', 'profile_gen', 'fieldC')
        self.connect('switchD', 'switchout', 'profile_gen', 'fieldD')
        self.connect('switchE', 'switchout', 'profile_gen', 'fieldE')
        self.connect('switchF', 'switchout', 'profile_gen', 'fieldF')
        self.connect('switchG', 'switchout', 'profile_gen', 'fieldG')
        self.connect('switchH', 'switchout', 'profile_gen', 'fieldH')
        self.connect('switchI', 'switchout', 'profile_gen', 'fieldI')

        self.connect('profile_gen', 'profile1', 'switchA', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchB', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchC', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchD', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchE', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchF', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchG', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchH', 'pla1profile')
        self.connect('profile_gen', 'profile1', 'switchI', 'pla1profile')

        self.connect('profile_gen', 'profile2', 'switchA', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchB', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchC', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchD', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchE', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchF', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchG', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchH', 'pla2profile')
        self.connect('profile_gen', 'profile2', 'switchI', 'pla2profile')

        # winning combination
        self.connect('switchA', 'pla1out', 'win_pla1', 'A')
        self.connect('switchB', 'pla1out', 'win_pla1', 'B')
        self.connect('switchC', 'pla1out', 'win_pla1', 'C')
        self.connect('switchD', 'pla1out', 'win_pla1', 'D')
        self.connect('switchE', 'pla1out', 'win_pla1', 'E')
        self.connect('switchF', 'pla1out', 'win_pla1', 'F')
        self.connect('switchG', 'pla1out', 'win_pla1', 'G')
        self.connect('switchH', 'pla1out', 'win_pla1', 'H')
        self.connect('switchI', 'pla1out', 'win_pla1', 'I')

        self.connect('switchA', 'pla2out', 'win_pla2', 'A')
        self.connect('switchB', 'pla2out', 'win_pla2', 'B')
        self.connect('switchC', 'pla2out', 'win_pla2', 'C')
        self.connect('switchD', 'pla2out', 'win_pla2', 'D')
        self.connect('switchE', 'pla2out', 'win_pla2', 'E')
        self.connect('switchF', 'pla2out', 'win_pla2', 'F')
        self.connect('switchG', 'pla2out', 'win_pla2', 'G')
        self.connect('switchH', 'pla2out', 'win_pla2', 'H')
        self.connect('switchI', 'pla2out', 'win_pla2', 'I')

        # all pressed
        self.connect('switchA', 'switchout', 'all_pressed', 'switchA')
        self.connect('switchB', 'switchout', 'all_pressed', 'switchB')
        self.connect('switchC', 'switchout', 'all_pressed', 'switchC')
        self.connect('switchD', 'switchout', 'all_pressed', 'switchD')
        self.connect('switchE', 'switchout', 'all_pressed', 'switchE')
        self.connect('switchF', 'switchout', 'all_pressed', 'switchF')
        self.connect('switchG', 'switchout', 'all_pressed', 'switchG')
        self.connect('switchH', 'switchout', 'all_pressed', 'switchH')
        self.connect('switchI', 'switchout', 'all_pressed', 'switchI')

        # one winner
        self.connect('win_pla1', 'won', 'one_win', 'pla1win')
        self.connect('win_pla2', 'won', 'one_win', 'pla2win')

        self.connect('one_win', 'pla1win_indicator', 'pla1win_indicator', '')
        self.connect('one_win', 'pla2win_indicator', 'pla2win_indicator', '')

        self.connect('all_pressed', 'allpressed', 'all_pressed_out', '')


if __name__ == '__main__':
    tictactoe = TicTacToe()
    sim = JIT(tictactoe, burst_size=1000, map_pins=True)


    def read_vals():
        print('turn player:',
              '1' if sim.get_pin_state('/profile_gen/profile1/pin') else '2')
        print('/switchA/switchout:',
              'X' if sim.get_pin_state(
                  '/switchA/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchA/pla2out/pin') else '')
        print('/switchB/switchout:',
              'X' if sim.get_pin_state(
                  '/switchB/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchB/pla2out/pin') else '')
        print('/switchC/switchout:',
              'X' if sim.get_pin_state(
                  '/switchC/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchC/pla2out/pin') else '')
        print('/switchD/switchout:',
              'X' if sim.get_pin_state(
                  '/switchD/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchD/pla2out/pin') else '')
        print('/switchE/switchout:',
              'X' if sim.get_pin_state(
                  '/switchE/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchE/pla2out/pin') else '')
        print('/switchF/switchout:',
              'X' if sim.get_pin_state(
                  '/switchF/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchF/pla2out/pin') else '')
        print('/switchG/switchout:',
              'X' if sim.get_pin_state(
                  '/switchG/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchG/pla2out/pin') else '')
        print('/switchH/switchout:',
              'X' if sim.get_pin_state(
                  '/switchH/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchH/pla2out/pin') else '')
        print('/switchI/switchout:',
              'X' if sim.get_pin_state(
                  '/switchI/pla1out/pin') else 'O' if sim.get_pin_state(
                  '/switchI/pla2out/pin') else '')

        print(''.join(['-' for _ in range(25)]))
        print('/pla1win_indicator/pin:', sim.get_pin_state('/pla1win_indicator/pin'))
        print('/pla2win_indicator/pin:', sim.get_pin_state('/pla2win_indicator/pin'))
        print('/all_pressed_out/pin:', sim.get_pin_state('/all_pressed_out/pin'))
        print(''.join(['-' for _ in range(25)]))
        print(''.join(['-' for _ in range(25)]))


    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchAin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchBin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchDin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchEin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchGin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchHin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchCin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchFin/pin', 1)
    sim.step()
    sim.step()
    read_vals()

    sim.set_pin_state('/switchIin/pin', 1)
    sim.step()
    sim.step()
    read_vals()
