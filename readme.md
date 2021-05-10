docker-compose up
docker-compose up --build
docker ps
docker exec -it flaskhello_flask_1 bash

http://0.0.0.0:5000//user/Mikhail
http://0.0.0.0:5000/submit
http://0.0.0.0:5000/iris/2,3,55,2
http://0.0.0.0:5000//show_image
http://0.0.0.0:5000/upload

curl --header "Content-Type: application/json" \
--request POST \
--data '{"flower":"1,2,3,7"}' \
http://localhost:5000/iris_post

### создать файл knn.pkl
docker exec -it flaskhello_flask_1 python train_model.py