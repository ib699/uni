package handler

import (
	"encoding/json"
	"fmt"
	"github.com/ib699/mid/model"
	"github.com/ib699/mid/repository"
	"net/http"
)

type UserHandler struct {
	Repo repository.Repository
}

func (h UserHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	username := r.Context().Value("username").(string)
	fmt.Println(r.URL.Path)
	if r.Method == http.MethodGet {
		if r.URL.Path == "/user" || r.URL.Path == "/user/" {
			all, err := h.Repo.GetUser(username)
			if err != nil {
				http.Error(w, "Cannot retrieve Users from database", http.StatusInternalServerError)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(all)
		} else if r.URL.Path == "/user/basket" || r.URL.Path == "/user/basket/" {
			all, err := h.Repo.GetByNameBasket(username)
			if err != nil {
				http.Error(w, "Cannot retrieve Users from database", http.StatusInternalServerError)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(all)
		}
	}

	if r.Method == http.MethodPatch {
		if r.URL.Path == "/user" || r.URL.Path == "/user/" {
			user, err := h.Repo.GetUser(username)

			var raw map[string]interface{}
			err = json.NewDecoder(r.Body).Decode(&raw)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			password, ok := raw["pass"].(string)
			if !ok {
				http.Error(w, "wrong keys", http.StatusBadRequest)
				return
			}

			temp := model.User{ID: 0, Username: username, Password: password}
			created, err := h.Repo.UpdateUser(user.ID, temp)
			if err != nil {
				http.Error(w, "Cannot create basket", http.StatusInternalServerError)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusCreated)
			json.NewEncoder(w).Encode(created)
		}
	}

	if r.Method == http.MethodDelete {
		err := h.Repo.DeleteUserByName(username)
		if err == repository.ErrDeleteFailed {
			http.Error(w, "No User with this id exists", http.StatusNotFound)
			return
		} else if err != nil {
			http.Error(w, "Cannot delete User", http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusNoContent)
	}
}
