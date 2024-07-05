package repository

import "github.com/ib699/mid/model"

type Repository interface {
	InitBasket() error
	CreateBasket(basket model.Basket) (*model.Basket, error)
	AllBasket() ([]model.Basket, error)
	GetByIdBasket(id int64) (*model.Basket, error)
	GetByNameBasket(name string) ([]model.Basket, error)
	UpdateBasket(id int64, updated model.Basket) (*model.Basket, error)
	DeleteBasket(id int64) error

	InitUser() error
	CreateUser(user model.User) (*model.User, error)
	CheckUserName(name string) error
	GetUser(name string) (*model.User, error)
	UpdateUser(id int64, updated model.User) (*model.User, error)
	DeleteUserByName(name string) error
}
