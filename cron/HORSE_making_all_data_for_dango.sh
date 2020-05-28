#!/bin/bash

BASE_DIR="/code"
LOG_DIR="${BASE_DIR}/log"
EXEC_NAME="HORSE_making_all_data_for_dango"

(echo "[`date`] Start executing ${EXEC_NAME}"; python -c "import ${EXEC_NAME}; ${EXEC_NAME}.lambda_handler('{}', 'context')"; echo "[`date`] Finish executing ${EXEC_NAME}") 2>&1 >${LOG_DIR}/${EXEC_NAME}_`date "+%Y_%m_%d"`.log

