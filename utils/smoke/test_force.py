#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES
# OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV
from base.Sequence import Sequence


class MainSequence(Sequence):
    def generate(self, **kargs):
        # Repeat the pair instruction_count times. Default stays at 1 so a
        # bare smoke run is still the short demo; the smoke list passes a
        # larger count.
        (count_opt, count_opt_valid) = self.getOption("instruction_count")
        count = int(count_opt) if count_opt_valid else 1
        for _ in range(count):
            self.genInstruction("ADD##RISCV")
            self.genInstruction("SRA##RISCV")


#  Points to the MainSequence defined in this file
MainSequenceClass = MainSequence

#  Using GenThreadRISCV by default, can be overriden with extended classes
GenThreadClass = GenThreadRISCV

#  Using EnvRISCV by default, can be overriden with extended classes
EnvClass = EnvRISCV
