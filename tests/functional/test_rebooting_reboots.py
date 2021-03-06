from nose import tools

from tests.functional import single_machine_test

class TestRebootingReboots(single_machine_test.SingleMachineTest):
    def run_check(self):
        self.depl.deploy()
        self.check_command("touch /run/not-rebooted")
        self.depl.reboot_machines(wait=True)
        m = self.depl.active.values()[0]
        m.check()
        tools.assert_equal(m.state, m.UP)
        tools.assert_false(self.check_command("test -f /run/not-rebooted"))
