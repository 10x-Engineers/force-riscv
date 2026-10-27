#!/usr/bin/env bash
#
# Generate one FORCE test per entry in the smoke list.
# Usage: utils/smoke/run_smoke_list.sh [smoke-list] [output-dir]
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LIST="${1:-${ROOT}/utils/smoke/smoke-list}"
OUT="${2:-${ROOT}/smoke-output}"
FRISCV="${ROOT}/bin/friscv"

if [[ ! -x "${FRISCV}" ]]; then
  echo "Missing ${FRISCV}. Build FORCE first (make && make tests)." >&2
  exit 1
fi
if [[ ! -f "${LIST}" ]]; then
  echo "Missing smoke list: ${LIST}" >&2
  exit 1
fi

rm -rf "${OUT}"
mkdir -p "${OUT}"
{
  echo "smoke_list=${LIST}"
  echo "git_sha=$(git -C "${ROOT}" rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "generated_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "name config template elf"
} > "${OUT}/INDEX.txt"

count=0
while IFS= read -r line || [[ -n "${line}" ]]; do
  line="${line%%#*}"
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "${line}" ]] && continue

  read -r name cfg template rest <<< "${line}"
  if [[ -z "${name}" || -z "${cfg}" || -z "${template}" ]]; then
    echo "Bad smoke-list line: ${line}" >&2
    exit 1
  fi
  [[ "${cfg}" != /* ]] && cfg="${ROOT}/${cfg}"
  [[ "${template}" != /* ]] && template="${ROOT}/${template}"
  if [[ ! -f "${cfg}" || ! -f "${template}" ]]; then
    echo "Missing config or template for ${name}: ${cfg} ${template}" >&2
    exit 1
  fi

  dest="${OUT}/${name}"
  mkdir -p "${dest}"
  echo "=== ${name}: ${cfg} ==="
  # shellcheck disable=SC2206
  extra=( ${rest:-} )
  (
    cd "${dest}"
    "${FRISCV}" --test "${template}" --cfg "${cfg}" --seed 1 "${extra[@]}"
  )
  elf="$(find "${dest}" -maxdepth 1 -name '*.Default.ELF' -size +0c | head -1)"
  if [[ -z "${elf}" ]]; then
    echo "No ELF produced for ${name}" >&2
    exit 1
  fi
  echo "${name} ${cfg#"${ROOT}/"} ${template#"${ROOT}/"} ${elf#"${ROOT}/"}" >> "${OUT}/INDEX.txt"
  count=$((count + 1))
done < "${LIST}"

if [[ "${count}" -eq 0 ]]; then
  echo "Smoke list has no entries: ${LIST}" >&2
  exit 1
fi
echo "Generated ${count} test(s) under ${OUT}"
