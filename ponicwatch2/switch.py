#!/bin/python3
"""
    Model for the table tb_switch.
    Created by Eric Gibert on 29 Apr 2016

    Switches are objects linked to a hardware pin (with or without a relay) to control an piece of equipment (pump, light,...).
    They belong to one Controller that controls their state.
    A switch is either set manually ON/OFF while in AUTO mode,the controller will tabulate the current time on the 'timer' string.
"""
from model.model import Ponicwatch_Table

class Switch(Ponicwatch_Table):
    """
    - 'switch_id' and 'name' identify uniquely a switch within a Controller database.
    - 'mode': indicates if the switch should be 'ON' or 'OFF' or 'AUTO'
        * at starting time, a switch of mode 'ON' will be set on, 'OFF' will be turn off (default)
        * in 'AUTO' mode, the scheduler assign the 'set_value_to' given in the 'init' dictionary to the pin
    - 'value': current state of the switch ( 0 = OFF, 1 = OFF )
    - 'init': identification of the hardware undelying the switch. Usually a pin number within an IC.
    - 'timer': cron like string to define the execution timing patterns
    - 'timer_interval': duration in  minutes of one timer unit, usually 15 minutes.
    """
    MODE = {
       -1: "INACTIVE",    # switch to be ignored
        0: "OFF",    # either the switch mode or the timer off
        1: "ON",     # either the switch mode or the timer on
        2: "AUTO",   # switch mode to automatic i.e. relies on current time & 'timer' to know the current value
    }

    META = {"table": "tb_switch",
            "id": "switch_id",
            "columns": (
                         "switch_id", # INTEGER NOT NULL,
                         "name", #  TEXT NOT NULL,
                         "mode", #  INTEGER NOT NULL DEFAULT (0),
                         "init", #  TEXT NOT NULL,
                         "timer", #  TEXT NOT NULL,
                         "value", #  INTEGER NOT NULL DEFAULT (0),
                         "timer_interval", #  INTEGER NOT NULL DEFAULT (15),
                         "updated_on", #  TIMESTAMP,
                         "synchro_on", #  TIMESTAMP
                        )
            }

    def __init__(self, controller, system_name, hardware, db=None, *args, **kwargs):
        super().__init__(db or controller.db, Switch.META, *args, **kwargs)
        self.controller = controller
        self.system_name = system_name + "/" + self["name"]
        self.hardware = hardware
        self.hardware.set_pin_as_output(self.init_dict["pin"])
        self.debug = max(self.controller.debug, self.init_dict.get("debug", 0))
        if self["mode"] > self.INACTIVE and self["timer"]:
            self.controller.add_cron_job(self.execute, self["timer"])
        # set the switch to 'set_value_to' if given in the init dictionary else to the last value recorded
        # try:
        #     self.execute(self.init_dict["set_value_to"])
        # except KeyError:
        #     self.execute(self.init_dict["value"])


    def execute(self, given_value=None):
        """
        On timer/scheduler: no 'given_value' hence set the pin to the 'set_value_to' found in the 'init' dictionary
        Else direct call: the pin is set to the 'given_value' if provided else the 'set_value'to' is used
        """
        if given_value is not None:
            try:
                set_to = self.init_dict["set_value_to"] if self.hardware["hardware"] == "ARRAY" else int(given_value)
                continue_execution = True
            except ValueError:
                self.controller.log.add_error(msg="given_value {} cannot be converted to int()".format(given_value),
                                              err_code=self["id"], fval=-2.1)
                continue_execution = False
        else: # automatic call by scheduler
            # if there is a 'if' condition then check it out first
            try:
                continue_execution = self.controller.eval_expression(submitted_by=self, if_expression=self.init_dict["if"])
            except KeyError:
                continue_execution = True

            # the value is a toggle: ON --> OFF --> ON --> OFF --> ....
            if self.init_dict["set_value_to"] in ('t', 'T'):
                set_to = abs(self.value - 1)         # abs(self["value"] - 1)
            # the value is define by the 'if' expression
            elif self.init_dict["set_value_to"] in ('b', 'B'):
                set_to = continue_execution
                continue_execution = True
            else: # the value is given in the switch definition i.e. 'hard coded'
                try:
                    # all values are possible for in memory array else must be integer
                    set_to = self.init_dict["set_value_to"] if self.hardware["hardware"] == "ARRAY" else int(self.init_dict["set_value_to"])
                except ValueError:
                    if self.debug >= 3:
                        print("Debug switch 01:", self.hardware, self.hardware["hardware"])
                    self.controller.log.add_error(msg="set_value_to {} must be int()".format(self.init_dict["set_value_to"]),
                                                  err_code=self["id"], fval=-2.3)
                    continue_execution = False

        if continue_execution:
            self.hardware.write(self.init_dict["pin"], set_to)
            self.update(value=set_to)
            self.controller.log.add_log(system_name=self.system_name, param=self)
        elif self.debug >= 3:
            print(self, "'if' condition False: abort execution")

    @property
    def value(self):
        """Read the switch position from the hardware directly - NO log"""
        val = self.hardware.read(self.init_dict["pin"], self.init_dict)
        return val if isinstance(val, int) else val[1]

    @classmethod
    def all_keys(cls, db):
        return super().all_keys(db, Switch.META)

    def __str__(self):
        return "{} ({})".format(self["name"], Switch.MODE[self["mode"]])
