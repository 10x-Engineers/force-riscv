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

# Instruction groups from the V 1.0 spec. Names match v_instructions.xml.
_GROUPS = {
    "int": (
        "VADD.VV##RISCV",
        "VADD.VX##RISCV",
        "VADD.VI##RISCV",
        "VSUB.VV##RISCV",
        "VAND.VV##RISCV",
        "VOR.VV##RISCV",
        "VXOR.VV##RISCV",
        "VSLL.VV##RISCV",
        "VSRL.VV##RISCV",
        "VSRA.VV##RISCV",
        "VMINU.VV##RISCV",
        "VMAXU.VV##RISCV",
        "VMSEQ.VV##RISCV",
        "VMSLTU.VV##RISCV",
        "VMV.V.V##RISCV",
        "VMV.V.X##RISCV",
        "VMV.V.I##RISCV",
    ),
    "widen": (
        "VWADD.VV##RISCV",
        "VWADDU.VV##RISCV",
        "VWSUB.VV##RISCV",
        "VWMUL.VV##RISCV",
        "VWMULU.VV##RISCV",
        "VWADD.WV##RISCV",
        "VSEXT.VF2##RISCV",
        "VZEXT.VF2##RISCV",
    ),
    "muldiv": (
        "VMUL.VV##RISCV",
        "VMULH.VV##RISCV",
        "VMULHU.VV##RISCV",
        "VMULHSU.VV##RISCV",
        "VDIV.VV##RISCV",
        "VDIVU.VV##RISCV",
        "VREM.VV##RISCV",
        "VREMU.VV##RISCV",
        "VMACC.VV##RISCV",
        "VNMSAC.VV##RISCV",
    ),
    "carry": (
        "VADC.VVM##RISCV",
        "VADC.VXM##RISCV",
        "VADC.VIM##RISCV",
        "VSBC.VVM##RISCV",
        "VSBC.VXM##RISCV",
        "VMADC.VVM##RISCV",
        "VMSBC.VVM##RISCV",
    ),
    "fixed": (
        "VSADD.VV##RISCV",
        "VSADDU.VV##RISCV",
        "VAADD.VV##RISCV",
        "VAADDU.VV##RISCV",
        "VSMUL.VV##RISCV",
        "VSSRA.VV##RISCV",
        "VSSRL.VV##RISCV",
        "VNCLIP.WV##RISCV",
        "VNCLIPU.WV##RISCV",
    ),
    "float": (
        "VFADD.VV##RISCV",
        "VFSUB.VV##RISCV",
        "VFMUL.VV##RISCV",
        "VFDIV.VV##RISCV",
        "VFMACC.VV##RISCV",
        "VFMAX.VV##RISCV",
        "VFMIN.VV##RISCV",
        "VFSGNJ.VV##RISCV",
        "VMFEQ.VV##RISCV",
        "VFCLASS.V##RISCV",
        "VFCVT.X.F.V##RISCV",
        "VFCVT.F.X.V##RISCV",
        "VFSQRT.V##RISCV",
        "VFREDUSUM.VS##RISCV",
    ),
    "mask": (
        "VMAND.MM##RISCV",
        "VMANDNOT.MM##RISCV",
        "VMOR.MM##RISCV",
        "VMXOR.MM##RISCV",
        "VMNAND.MM##RISCV",
        "VCPOP.M##RISCV",
        "VFIRST.M##RISCV",
        "VMSBF.M##RISCV",
        "VMSIF.M##RISCV",
        "VMSOF.M##RISCV",
        "VIOTA.M##RISCV",
        "VID.V##RISCV",
    ),
    "permute": (
        "VSLIDEUP.VI##RISCV",
        "VSLIDEDOWN.VX##RISCV",
        "VSLIDE1UP.VX##RISCV",
        "VSLIDE1DOWN.VX##RISCV",
        "VRGATHER.VV##RISCV",
        "VRGATHEREI16.VV##RISCV",
        "VCOMPRESS.VM##RISCV",
        "VMV1R.V##RISCV",
        "VMV2R.V##RISCV",
    ),
    "reduce": (
        "VREDSUM.VS##RISCV",
        "VREDMAX.VS##RISCV",
        "VREDMINU.VS##RISCV",
        "VREDAND.VS##RISCV",
        "VREDXOR.VS##RISCV",
        "VWREDSUM.VS##RISCV",
    ),
}


class MainSequence(Sequence):
    def generate(self, **kargs):
        count = self._opt_int("instruction_count", 256)
        vsew = self._opt_int("vsew", 2)
        vlmul = self._opt_int("vlmul", 0)
        group = self._opt_str("group", "int")
        ops = _GROUPS.get(group)
        if ops is None:
            self.error("Unknown vector group %s" % group)

        self._lock_field("vtype.VSEW", vsew, 8)
        self._lock_field("vtype.VLMUL", vlmul, 8)
        vta = self._opt_int("vta", None)
        vma = self._opt_int("vma", None)
        if vta is not None:
            self._lock_field("vtype.VTA", vta, 2)
        if vma is not None:
            self._lock_field("vtype.VMA", vma, 2)

        vm = self._opt_int("vm", None)
        for _ in range(count):
            instr = self.choice(ops)
            params = {}
            if vm is not None and self._accepts_mask(instr):
                params["vm"] = vm
            self.genInstruction(instr, params)

    def _opt_int(self, name, default):
        (value, valid) = self.getOption(name)
        if not valid:
            return default
        return int(value)

    def _opt_str(self, name, default):
        (value, valid) = self.getOption(name)
        if not valid:
            return default
        return str(value)

    def _lock_field(self, tree_name, selected, span):
        choices_mod = ChoicesModifier(self.genThread)
        weights = {"0x%x" % i: (10 if i == selected else 0) for i in range(span)}
        choices_mod.modifyRegisterFieldValueChoices(tree_name, weights)
        choices_mod.commitSet()

    def _accepts_mask(self, instr):
        if instr.startswith("VMV.V.") or instr.startswith("VMV") and "R.V" in instr:
            return False
        if ".MM##" in instr or instr.startswith(("VCPOP", "VFIRST", "VSET")):
            return False
        return True


MainSequenceClass = MainSequence
GenThreadClass = GenThreadRISCV
EnvClass = EnvRISCV
