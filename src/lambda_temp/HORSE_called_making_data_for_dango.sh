#!/bin/bash

BASE_DIR="/code/lambda_temp"
LOG_DIR="${BASE_DIR}/log"
EXEC_NAME="HORSE_called_making_data_for_dango"

NEXT_CAL_FILE="next_week_calendar.csv"
DATE_LIST=()
DATE_LIST_FILE="date_list.txt"

aws s3 cp s3://rpa-horse-racing/${NEXT_CAL_FILE} ${BASE_DIR}/
awk -F ',' 'NR>=2 {print $2}' ${NEXT_CAL_FILE} >${DATE_LIST_FILE}

while read LINE
do
  DATE_LIST+=("${LINE}")
done < ${DATE_LIST_FILE}

for DATE in ${DATE_LIST[@]}
do
  (echo "[`date`] Start executing ${EXEC_NAME}"; python -c "import ${EXEC_NAME}; ${EXEC_NAME}.lambda_handler(${DATE}, 'context')"; echo "[`date`] Finish executing ${EXEC_NAME}") 2>&1 >${LOG_DIR}/${EXEC_NAME}_${DATE}.log &
done

