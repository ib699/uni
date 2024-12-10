package main

import (
	"database/sql"
	"fmt"
	"github.com/ib699/mid/handler"
	"github.com/ib699/mid/repository"
	"github.com/ib699/mid/service"
	_ "github.com/lib/pq"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"net/http"
)

const dbType = "postgres"

func main() {
	var db *sql.DB
	var err error
	var basketRepo repository.Repository
	var userRepo repository.Repository

	switch dbType {
	case "postgres":
		connStr := "postgres://lwall:yourpassword@localhost/web?sslmode=disable"
		db, err = sql.Open("postgres", connStr)
		if err != nil {
			log.Fatal(err)
		}
		basketRepo = repository.NewPostgreSQLRepository(db)
		userRepo = repository.NewPostgreSQLRepository(db)
	case "sqlite":
		db, err = sql.Open("sqlite3", "sqlite.db")
		if err != nil {
			log.Fatal(err)
		}
		basketRepo = repository.NewSQLiteRepository(db)
		userRepo = repository.NewSQLiteRepository(db)
	default:
		log.Fatal("DB_TYPE variable not set")
	}

	if err := basketRepo.InitBasket(); err != nil {
		log.Fatal(err)
	}

	if err := userRepo.InitUser(); err != nil {
		log.Fatal(err)
	}

	basketHandler := handler.BasketHandler{Repo: basketRepo, DbType: dbType}
	userHandler := handler.UserHandler{Repo: userRepo}
	authHandler := handler.AuthHandler{Repo: userRepo}

	fmt.Println("Starting server")
	http.Handle("/login/", authHandler)
	http.Handle("/create/", authHandler)
	http.Handle("/basket/", service.AuthMiddleware(basketHandler))
	http.Handle("/user/", service.AuthMiddleware(userHandler))
	fmt.Println(http.ListenAndServe(":8080", nil))
}
