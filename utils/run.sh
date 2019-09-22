#!/usr/bin/env bash

main() {
    local o opts
    local buildroot_dir br2_external_dir logfile output_dir python_interpreter

    o='b:e:l:o:p:'
    opts="$(getopt -n "${my_name}" -o "${o}" -- "${@}")"
    eval set -- "${opts}"

    while [ ${#} -gt 0 ]; do
        case "${1}" in
        (-b)
            buildroot_dir="$(readlink -f "${2}")"; shift 2
            ;;
        (-e)
            br2_external_dir="$(readlink -f "${2}")"; shift 2
            ;;
        (-l)
            logfile="${2}"; shift 2
            ;;
        (-o)
            output_dir="$(readlink -f "${2}")"; shift 2
            ;;
        (-p)
            python_interpreter="${2}"; shift 2
            ;;
        (--)
            shift; break
            ;;
        esac
    done
    if [ ! -e "${buildroot_dir}/DEVELOPERS" ]; then
        printf "error: %s: not a buildroot repo\n" "${buildroot_dir}" >&2; exit 1
    fi
    if [ ! -e "${br2_external_dir}/external.desc" ]; then
        printf "error: %s: not a br2-external\n" "${br2_external_dir}" >&2; exit 1
    fi
    if [ ! -e "${output_dir}/.br2-external.mk" ]; then
        printf "error: %s: not an output dir\n" "${output_dir}" >&2; exit 1
    fi
    if [ ! -z "${python_interpreter}" ]; then
        if ! which "${python_interpreter}"; then
            printf "error: %s: not callable\n" "${python_interpreter}" >&2; exit 1
        fi
    fi
    if [ ! -d $(dirname "${logfile}") ]; then
        printf "error: %s: logfile cannot be created\n" "${logfile}" >&2; exit 1
    fi

    {
        cd "${buildroot_dir}"
        ${python_interpreter} ./utils/check-package --help
        ${python_interpreter} ./utils/check-package -vvv $(git ls-files -- package) || true
        cd "${br2_external_dir}"
        ${python_interpreter} "${buildroot_dir}/utils/check-package" -b -vvv $(git ls-files -- package) | \
            sed -e "s,^${br2_external_dir}/,,g" \
            || true
    } 1>"${logfile}"
}

my_name="${0##*/}"
main "${@}"
