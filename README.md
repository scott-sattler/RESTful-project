
# RESTful-project
RESTful microservices

frontend <-> gateway <-> backend

frontend serves html

frontend communicates with backend exclusively through gateway

backend communicates with frontend exclusively through gateway

backend stores files if necessary, does computation, etc.

backend currently includes a color_lookup service


gateway routes (planned functionality expansion)


## TO USE:
run microservices/run_servers.bat
open webpage 127.0.0.1:5075/index.html
upload local image, pick color with mouse
