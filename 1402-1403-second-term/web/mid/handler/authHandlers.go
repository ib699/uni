package handler

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/ib699/mid/model"
	"github.com/ib699/mid/repository"
	"github.com/ib699/mid/service"
	"net/http"
)

type AuthHandler struct {
	Repo repository.Repository
}

func (h AuthHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.URL.Path)
	if r.URL.Path == "/login/" {
		if r.Method == http.MethodPost {
			var raw map[string]interface{}
			err := json.NewDecoder(r.Body).Decode(&raw)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			username, ok1 := raw["user"].(string)
			password, ok2 := raw["pass"].(string)

			if !ok1 || !ok2 {
				http.Error(w, "wrong keys", http.StatusBadRequest)
				return
			}

			user, err := h.Repo.GetUser(username)
			if err == repository.ErrNotExists {
				http.Error(w, "User not found", http.StatusNotFound)
				return
			}
			if err != nil {
				http.Error(w, "Cannot return User", http.StatusInternalServerError)
				return
			}
			if user.Password != password {
				http.Error(w, "Wrong password", http.StatusForbidden)
				return
			}

			token, err := service.GenerateJWTToken(username, password)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}
			w.WriteHeader(http.StatusCreated)
			json.NewEncoder(w).Encode(token)
		}
	}
	if r.URL.Path == "/create/" {
		if r.Method == http.MethodPost {
			var raw map[string]interface{}
			err := json.NewDecoder(r.Body).Decode(&raw)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			username, ok1 := raw["user"].(string)
			password, ok2 := raw["pass"].(string)

			if !ok1 || !ok2 {
				http.Error(w, "wrong keys", http.StatusBadRequest)
				return
			}

			err = h.Repo.CheckUserName(username)
			if !errors.Is(err, repository.ErrNotExists) {
				http.Error(w, "User Duplicate", http.StatusNotFound)
				return
			}

			token, err := service.GenerateJWTToken(username, password)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			temp := model.User{ID: 0, Username: username, Password: password}
			h.Repo.CreateUser(temp)
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusCreated)
			json.NewEncoder(w).Encode(token)
		}
	}
}
