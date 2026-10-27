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
from VectorTestSequence import VectorTestSequence
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV


# Whole-register moves and round-toward-zero vector conversions from the V spec.
class MainSequence(VectorTestSequence):
    def __init__(self, aGenThread, aName=None):
        super().__init__(aGenThread, aName)
        self._mInstrList = (
            "VMV.V.V##RISCV",
            "VMV.V.X##RISCV",
            "VMV.V.I##RISCV",
            "VFMV.V.F##RISCV",
            "VFCVT.RTZ.X.F.V##RISCV",
            "VFCVT.RTZ.XU.F.V##RISCV",
            "VFWCVT.RTZ.X.F.V##RISCV",
            "VFWCVT.RTZ.XU.F.V##RISCV",
            "VFNCVT.RTZ.X.F.W##RISCV",
            "VFNCVT.RTZ.XU.F.W##RISCV",
        )

    def generate(self, **kargs):
        for instr in self._mInstrList:
            instr_id = self.genInstruction(instr)
            if not instr_id:
                self.error("Instruction %s did not generate correctly" % instr)

    def _getInstructionList(self):
        return self._mInstrList


MainSequenceClass = MainSequence
GenThreadClass = GenThreadRISCV
EnvClass = EnvRISCV
