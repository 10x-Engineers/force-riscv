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
from base.ChoicesModifier import ChoicesModifier
from base.Sequence import Sequence
from riscv.EnvRISCV import EnvRISCV
from riscv.GenThreadRISCV import GenThreadRISCV

# Single-width integer vector ops. These stay legal across the SEW/LMUL
# combinations listed in utils/smoke/smoke-list.
_VECTOR_OPS = (
    "VADD.VV##RISCV",
    "VADD.VX##RISCV",
    "VADD.VI##RISCV",
    "VSUB.VV##RISCV",
    "VSUB.VX##RISCV",
    "VAND.VV##RISCV",
    "VAND.VX##RISCV",
    "VOR.VV##RISCV",
    "VXOR.VV##RISCV",
    "VSLL.VV##RISCV",
    "VSLL.VI##RISCV",
    "VSRL.VV##RISCV",
    "VSRA.VV##RISCV",
    "VMIN.VV##RISCV",
    "VMAX.VV##RISCV",
    "VMV.V.V##RISCV",
    "VMV.V.X##RISCV",
    "VMV.V.I##RISCV",
)


class MainSequence(Sequence):
    def generate(self, **kargs):
        (count_opt, count_valid) = self.getOption("instruction_count")
        count = int(count_opt) if count_valid else 256
        (vsew_opt, vsew_valid) = self.getOption("vsew")
        (vlmul_opt, vlmul_valid) = self.getOption("vlmul")
        vsew = int(vsew_opt) if vsew_valid else 2
        vlmul = int(vlmul_opt) if vlmul_valid else 0
        self._lock_vtype(vsew, vlmul)

        for _ in range(count):
            self.genInstruction(self.choice(_VECTOR_OPS))

    def _lock_vtype(self, vsew, vlmul):
        choices_mod = ChoicesModifier(self.genThread)
        vsew_weights = {"0x%x" % i: (10 if i == vsew else 0) for i in range(8)}
        vlmul_weights = {"0x%x" % i: (10 if i == vlmul else 0) for i in range(8)}
        choices_mod.modifyRegisterFieldValueChoices("vtype.VSEW", vsew_weights)
        choices_mod.modifyRegisterFieldValueChoices("vtype.VLMUL", vlmul_weights)
        choices_mod.commitSet()


MainSequenceClass = MainSequence
GenThreadClass = GenThreadRISCV
EnvClass = EnvRISCV
