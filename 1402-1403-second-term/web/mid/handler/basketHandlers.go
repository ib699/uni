package handler

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/ib699/mid/model"
	"github.com/ib699/mid/repository"
	"net/http"
	"strconv"
	"strings"
	"time"
)

type BasketHandler struct {
	Repo   repository.Repository
	DbType string
}

func (h BasketHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	username := r.Context().Value("username").(string)
	fmt.Println(r.URL.Path)
	if r.Method == http.MethodGet {
		if r.URL.Path == "/basket" || r.URL.Path == "/basket/" {
			all, err := h.Repo.AllBasket()
			if err != nil {
				http.Error(w, "Cannot retrieve baskets from database", http.StatusInternalServerError)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(all)
		} else {
			id, err := strconv.ParseInt(strings.TrimPrefix(r.URL.Path, "/basket/"), 10, 64)
			if err != nil {
				http.Error(w, "wrong id", http.StatusBadRequest)
				return
			}

			basket, err := h.Repo.GetByIdBasket(id)
			if err == repository.ErrNotExists {
				http.Error(w, "basket not found", http.StatusNotFound)
				return
			}
			if err != nil {
				http.Error(w, "Cannot return basket", http.StatusInternalServerError)
				return
			}

			basket.BasketData = basket.BasketData
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(basket)
		}
	}

	if r.Method == http.MethodPost {
		var raw map[string]interface{}
		err := json.NewDecoder(r.Body).Decode(&raw)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		currentTime := time.Now().Format("2006-01-02 15:04:05")
		data, ok1 := raw["data"].(string)
		status, ok2 := raw["status"].(string)

		if !ok1 || !ok2 {
			http.Error(w, "wrong keys", http.StatusBadRequest)
			return
		}

		if sizeErr := checkStringSize(data); sizeErr != nil {
			http.Error(w, "data is to long", http.StatusBadRequest)
			return
		}
		if status != "PENDING" && status != "COMPLETED" {
			http.Error(w, "unknown status for basket", http.StatusBadRequest)
			return
		}

		err = h.Repo.CheckUserName(username)
		if err == repository.ErrNotExists {
			http.Error(w, "User not found", http.StatusNotFound)
			return
		}
		if err != nil {
			http.Error(w, "Cannot update User", http.StatusInternalServerError)
			return
		}

		temp := model.Basket{ID: 0, CreatedAt: currentTime, User: username, UpdatedAt: currentTime, BasketData: data, Status: status}
		created, err := h.Repo.CreateBasket(temp)
		if err != nil {
			http.Error(w, "Cannot Create basket", http.StatusInternalServerError)
			return
		}
		created.BasketData = data
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(created)
	}

	if r.Method == http.MethodPatch {
		id, err := strconv.ParseInt(strings.TrimPrefix(r.URL.Path, "/basket/"), 10, 64)
		if err != nil {
			http.Error(w, "wrong id", http.StatusBadRequest)
			return
		}

		previous, err := h.Repo.GetByIdBasket(id)
		if err == repository.ErrNotExists {
			http.Error(w, "basket not found", http.StatusNotFound)
			return
		}
		if err != nil {
			http.Error(w, "Cannot update basket", http.StatusInternalServerError)
			return
		}
		if previous.Status == "COMPLETED" {
			http.Error(w, "Can't update basket with state Completed", http.StatusConflict)
			return
		}

		var raw map[string]interface{}
		err = json.NewDecoder(r.Body).Decode(&raw)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		currentTime := time.Now().Format("2006-01-02 15:04:05")
		data, ok1 := raw["data"].(string)
		status, ok2 := raw["status"].(string)

		if !ok1 || !ok2 {
			http.Error(w, "wrong keys", http.StatusBadRequest)
			return
		}
		if sizeErr := checkStringSize(data); sizeErr != nil {
			http.Error(w, "data is to long", http.StatusBadRequest)
			return
		}
		if status != "PENDING" && status != "COMPLETED" {
			http.Error(w, "unknown status for basket", http.StatusBadRequest)
			return
		}

		updated := model.Basket{ID: previous.ID, CreatedAt: previous.CreatedAt, User: username, UpdatedAt: currentTime, BasketData: data, Status: status}
		upd, err := h.Repo.UpdateBasket(id, updated)
		if err != nil {
			http.Error(w, "Cannot update basket", http.StatusInternalServerError)
			return
		}
		upd.BasketData = data
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(upd)
	}

	if r.Method == http.MethodDelete {
		id, err := strconv.ParseInt(strings.TrimPrefix(r.URL.Path, "/basket/"), 10, 64)
		if err != nil {
			http.Error(w, "wrong id", http.StatusBadRequest)
			return
		}

		err = h.Repo.DeleteBasket(id)
		if err == repository.ErrDeleteFailed {
			http.Error(w, "No basket with this id exists", http.StatusNotFound)
			return
		} else if err != nil {
			http.Error(w, "Cannot delete basket", http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusNoContent)
	}
}

func checkStringSize(s string) error {
	if len(s) > 2048 {
		return errors.New("String size exceeds the limit")
	}
	return nil
}
