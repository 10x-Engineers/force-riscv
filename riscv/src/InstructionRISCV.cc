//
// Copyright (C) [2020] Futurewei Technologies, Inc.
//
// FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
// FIT FOR A PARTICULAR PURPOSE.
// See the License for the specific language governing permissions and
// limitations under the License.
//
#include <InstructionRISCV.h>
#include <InstructionConstraintRISCV.h>
#include <OperandRISCV.h>
#include <RetOperandRISCV.h>
#include <Generator.h>
#include <GenRequest.h>
#include <Log.h>

/*!
  \file InstructionRISCV.cc
  \brief Code supporting RISCV specific instruction generation
*/

using namespace std;

namespace Force {

  void RetInstruction::Setup(const GenInstructionRequest& instrReq, Generator& gen)
  {
    Instruction::Setup(instrReq, gen);
  }

  bool RetInstruction::GetPrePostAmbleRequests(Generator& gen) const
  {
    if (NoRestriction())
    {
      LOG(notice) << "{RetInstruction::GetPrePostAmbleRequests} No restriction, bypassing..." << endl;
      return false;
    }

    LOG(notice) << "{RetInstruction::GetPrePostAmbleRequests}" << endl;
    auto opr = FindOperandType<RetOperand>();
    if (nullptr != opr)
    {
      return opr->GetPrePostAmbleRequests(gen);
    }
    else
    {
      LOG(notice) << "{RetInstruction::GetPrePostAmbleRequests} - can't find RetOperand" << endl;
      return false;
    }
  }

  InstructionConstraint* RetInstruction::InstantiateInstructionConstraint() const
  {
    return new RetInstructionConstraint();
  }

}
