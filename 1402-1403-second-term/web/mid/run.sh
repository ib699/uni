#!/usr/bin/env bash
source setup.sh

read -p "1)Create User 2)Login & Run Tests: " mode

if [ $mode == "1" ]; then
    read -p "Username: " u
    read -p "Password: " p
    curl -X POST http://localhost:8080/create/ -H "Content-Type: application/json" -d "{\"user\": \"$u\", \"pass\": \"$p\"}"
    exit 1
elif [ $mode == "2" ]; then
    read -p "Username: " u
    read -p "Password: " p
    or_token=$(curl -X POST http://localhost:8080/login/ -H "Content-Type: application/json" -d "{\"user\": \"$u\", \"pass\": \"$p\"}")

    if [ -z "$or_token" ] || [ "$or_token" == "Wrong password" ] || [ "$or_token" == "User not found" ]; then
        echo "Bad Request. Please login first."
        exit 1
    fi

    token=$(echo $or_token | sed 's/^"\{1\}//;s/"\{1\}$//')

    # get all id's
    curl http://localhost:8080/basket/ -H "Authorization: $token"

    # create id
    curl -X POST http://localhost:8080/basket/ -H "Authorization: $token" -H "Content-Type: application/json" -d '{"data": "{\"fuck jack\": \"hello fucker\"}", "status": "PENDING"}'

    # get id
    curl http://localhost:8080/basket/1 -H "Authorization: $token"

    # update id
    curl -X PATCH http://localhost:8080/basket/1 -H "Authorization: $token" -H "Content-Type: application/json" -d '{"data": "{\"fuck john\": \"hello john fucker\"}", "status": "COMPLETED"}'

    # get all id's
    curl http://localhost:8080/user/ -H "Authorization: $token"

    # get id
    curl http://localhost:8080/user/basket/ -H "Authorization: $token"

    # update id
    curl -X PATCH http://localhost:8080/user/ -H "Authorization: $token" -H "Content-Type: application/json" -d '{"pass": "hello mate"}'

    read -p "Delete Basket?(y)" del
    if [ $del == "y" ]; then
      # delete basket
      curl -X DELETE http://localhost:8080/basket/1 -H "Authorization: $token"
    fi

    read -p "Delete User?(y)" del
    if [ $del == "y" ]; then
      # delete user
     curl -X DELETE http://localhost:8080/user/ -H "Authorization: $token"
    fi
else
    echo "Bad input. Please select a valid option."
fi