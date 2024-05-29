# The actual commands we want to execute.
cd services/backend && flask run & \
cd services/frontend && npm run dev & \

# Trap the input and wait for the script to be cancelled.
waitforcancel
return 0
