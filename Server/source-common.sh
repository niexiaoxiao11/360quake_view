# (C) 2022 HelpSystems. All rights reserved.
# ------------------------------------------------------------------
# BASH source routines for common support
# ------------------------------------------------------------------

export CS_DELIMITER="--------------------------------------------------------------------------------"

# make pretty looking messages (thanks Carlos)
function print_good () {
    echo -e "\x1B[01;32m[+]\x1B[0m $1"
}

function print_error () {
    echo -e "\x1B[01;31m[-]\x1B[0m $1"
}

function print_info () {
    echo -e "\x1B[01;34m[*]\x1B[0m $1"
}

# ------------------------------------------------------------------
# Print a simple header to console
# ------------------------------------------------------------------
# $1 = Header Text
# ------------------------------------------------------------------
function print_section_header () {
  echo
  print_info "${1}"
}
