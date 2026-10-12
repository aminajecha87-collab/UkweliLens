#!/bin/bash
#tool name: system information (sysinfo)
#description: find and display linux system information about CPU, RAM, disk.
#define color codes for clean output in the terminal.
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' #no color

#function to display to the users after entering sysinfo
show_myusers() {
echo -e "${PURPLE}================================================="
echo -e "${RED} LINUX ${GREEN} SYSTEM ${BLUE} INFORMATION"
echo -e "${PURPLE}================================================"
}

#function to display when user type -h or --help
show_help() {
echo -e "${YELLOW} condition to use: ${NC} sysinfo [OPTION]"
echo -e "\n ${YELLOW} Options available are: "
echo -e " ${GREEN} -c, --cpu ${NC} CPU details"
echo -e "${GREEN} -m, --ram ${NC} Total, Used, Free Memory usage"
echo -e "${GREEN} -d, --disk ${NC} Disk storage utilization"
echo -e "${GREEN} -a, --all ${NC} All system information"
echo -e "${GREEN} -h, --help ${NC} show all instructions"
}

# Function to Extract and format CPU specifications and load
get_cpu_info() {
    echo -e "\n${YELLOW} C${BLUE}P${PURPLE}U${RED} PERFORMANCE ${PURPLE} METRICS ]${NC}"
    echo "--------------------------------------------------"
    # Defensive Error Handling: Verify if the 'lscpu' binary exists before calling it
    if command -v lscpu &> /dev/null; then
        lscpu | grep -E "Model name|CPU\(s\):|Thread\(s\) per core"
        echo -e "${GREEN}Current Load Average:${NC} $(uptime | awk -F'load average:' '{ print $2 }')"
    else
        echo -e "${RED} ERROR: 'lscpu' utility is missing on this platform.${NC}"
    fi
}

#Function to get memory info  in human readable form 
get_ram_info(){
echo "--------------------------------------------------"
echo -e "$\n ${YELLOW}R${BLUE}A${PURPLE}M${RED} UTILIZATION ${NC} METRICS"
free -h
}

#function to get filesystem storage statistics
get_disk_info(){
echo "--------------------------------------------------"
echo -e "\n ${YELLOW} D${BLUE}I${PURPLE}S${RED}K${GREEN} STORAGE ${NC} UTILIZATION"
df -h --total | grep -E "Filesystem|total"
}

#function to get all informations
get_all_info(){
show_myusers
CURRENT_DATE=$(date "+%A, %B %d %Y - %I:%M %p")
echo -e "${GREEN} REPORT ${PURPLE} GENERATED ${BLUE} ON: ${NC} $(date "+%A, %B %d, %Y - %I:%M %p")"
get_cpu_info
get_ram_info
get_disk_info
}

#function when a user didnt choose any flag via CLI
our_menu(){
show_myusers
echo -e "\n ${YELLOW} Please choose options as from this menu:"
echo -e "${GREEN}c ${NC}  CPU Information"
echo -e "${GREEN}m ${NC}  Memory Utilization"
echo -e "${GREEN}d ${NC}  Disk Space"
echo -e "${GREEN}a ${NC}  Full System Report"
echo -e "${RED}e ${NC}    Exit Tool"

read -p " Enter your choice (c / m / d / a / e): " choice

    # Map the captured choice string using a case routing architecture
    case $choice in
        c) get_cpu_info ;;
        m) get_ram_info ;;
        d) get_disk_info ;;
        a) get_all_info ;;
        e) echo -e "${GREEN} Exiting, Welcome again!"; exit 0 ;;
        *) echo -e "${RED} ERROR: Invalid selection. Please use c, m, d, a, or e."; exit 1 ;;
    esac
}

if [ $# -eq 0 ]; then
    # Route to prompt engine if no positional parameter arguments exist
    our_menu
else
    # Intercept specific input automation arguments ($1)
    case "$1" in
        -c|--cpu)    get_cpu_info ;;
        -m|--ram)    get_ram_info ;;
        -d|--disk)   get_disk_info ;;
        -a|--all)    get_all_info ;;
        -h|--help)   show_help ;;
        *)           echo -e "${RED} ERROR: Unrecognized command argument '$1'.${NC}" >&2
                     show_help  exit 1;;
    esac
fi


