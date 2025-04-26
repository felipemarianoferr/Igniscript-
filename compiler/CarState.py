import time
import math

class CarState:
    def __init__(self, initial_horsepower=120):
        try:
            initial_horsepower_float = float(initial_horsepower)
            if initial_horsepower_float <= 0:
                raise ValueError("Horsepower must be positive.")
            self.cavalos = initial_horsepower_float
        except ValueError:
            raise ValueError("Initial horsepower must be a number.")

        self.gasolina = 100.0
        self.rpm = 0
        self.ligado = False
        self.marcha = 0 # Start in Neutral
        self.rpm_limits = {0: 0, 1: 2000, 2: 4000, 3: 6000, 4: 8000, 5: 10000}
        self.base_delay = 0.1
        self.base_gas_consumption = 1.0
        self.reference_horsepower = 120.0
        self.engine_ops = {"BinOp", "UnOp", "While", "If"}

    def _check_gas(self, operation_description):
        if self.gasolina <= 1e-9:
             self.ligado = False
             raise Exception(f"RuntimeError: Out of gas! Cannot perform '{operation_description}'. Engine turned off.")

    def _check_engine_status(self, operation_description):
        if not self.ligado:
            raise Exception(f"RuntimeError: Engine is off! Cannot perform '{operation_description}'.")

    def _check_gear_status(self, operation_description):
         if self.marcha == 0:
              raise Exception(f"RuntimeError: Cannot perform '{operation_description}' while in Neutral (gear 0).")

    def _check_rpm_limit(self, operation_description):
        if self.marcha > 0 and self.rpm >= self.rpm_limits[self.marcha]:
            self.ligado = False
            raise Exception(f"RuntimeError: RPM limit ({self.rpm_limits[self.marcha]}) exceeded for gear {self.marcha} during '{operation_description}'! Engine damaged and turned off.")

    def _perform_delay(self):
         try:
              if self.cavalos <= 1e-9:
                  delay = self.base_delay
              else:
                  delay = self.base_delay / (self.cavalos / self.reference_horsepower)
              time.sleep(max(0, delay))
         except ZeroDivisionError:
              raise Exception("InternalError: Reference horsepower is zero, cannot calculate delay.")


    def notify_engine_required_operation(self, operation_type_name):
        self._check_engine_status(operation_type_name)
        self._check_gas(operation_type_name)
        requires_gear_check = False
        for op_type in self.engine_ops:
            if operation_type_name.startswith(op_type):
                requires_gear_check = True
                break
        if requires_gear_check:
             self._check_gear_status(operation_type_name)
        self._check_rpm_limit(operation_type_name)

    def consume_resources(self, operation_type_name):
        factor = 1.0
        if self.cavalos > 1e-9:
             factor = self.cavalos / self.reference_horsepower

        gas_cost_float = self.base_gas_consumption * factor
        gas_consumed_this_op = math.floor(gas_cost_float)

        if self.base_gas_consumption >= 1.0:
             gas_consumed_this_op = max(1, gas_consumed_this_op)
        else:
             gas_consumed_this_op = max(0, gas_consumed_this_op)

        if self.gasolina < gas_consumed_this_op:
             self._check_gas(f"consuming resources for {operation_type_name}")

        self.gasolina -= gas_consumed_this_op
        self.rpm += 100
        self._perform_delay()
        self._check_rpm_limit(f"completion of {operation_type_name}")

        if self.gasolina <= 1e-9:
             self.ligado = False

    def set_engine_on_off(self, status_bool):
        # Only change ligado status, do not touch RPM here
        if status_bool is True and self.ligado is False:
             self._check_gas("Turning engine on")
             self.ligado = True
             
        elif status_bool is False and self.ligado is True:
             self.ligado = False
             
        elif status_bool == self.ligado:
             pass
        else:
             pass


    def set_gear(self, target_gear):
        operation_description = f"Setting gear to {target_gear}"
        self._check_engine_status(operation_description)

        try:
            target_gear_int = int(target_gear)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid gear value: {target_gear}. Must be an integer.")

        if target_gear_int not in self.rpm_limits:
            raise ValueError(f"Invalid gear: {target_gear_int}. Must be between 0 and {len(self.rpm_limits)-1}.")

        if self.marcha != target_gear_int:
             if target_gear_int > 0 and self.rpm >= self.rpm_limits[target_gear_int]:
                  self.ligado = False
                  raise Exception(f"RuntimeError: RPM ({self.rpm}) already exceeds limit ({self.rpm_limits[target_gear_int]}) for target gear {target_gear_int}! Cannot shift. Engine damaged and turned off.")
             self.marcha = target_gear_int


    def set_horsepower(self, new_power):
         try:
             new_power_float = float(new_power)
             if new_power_float <= 0:
                  raise ValueError("Horsepower must be positive.")
             self.cavalos = new_power_float
         except (ValueError, TypeError):
              raise ValueError(f"Invalid horsepower value: {new_power}. Must be a positive number.")


    def get_state_info(self):
        state_str = (
            f"--- Car State ---\n"
            f"  Engine: {'carOn' if self.ligado else 'carOff'}\n"
            f"  Gasolina: {self.gasolina:.2f} L\n"
            f"  RPM: {self.rpm}\n"
            f"  Marcha: {self.marcha}\n"
            f"  Cavalos: {self.cavalos}\n"
            f"-----------------"
        )
        return state_str