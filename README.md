
# RESTful-Project
RESTful Microservices Project

frontend <-> gateway <-> backend

frontend serves html</br>
frontend communicates with backend exclusively through gateway

backend communicates with frontend exclusively through gateway</br>
backend stores files if necessary, does computation, etc.</br>
backend currently includes a color_lookup service

gateway routes (planned functionality expansion)

## TO USE:
1. run microservices/run_servers.bat</br>
2. open webpage 127.0.0.1:5075/index.html</br>
3. upload local image, pick color with mouse</br>
