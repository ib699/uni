package repository

import (
	"database/sql"
	"encoding/json"
	"errors"
	"github.com/ib699/mid/model"
)

type PostgreSQLRepository struct {
	Db *sql.DB
}

func NewPostgreSQLRepository(db *sql.DB) *PostgreSQLRepository {
	return &PostgreSQLRepository{Db: db}
}

func (r *PostgreSQLRepository) InitBasket() error {
	query := `
    CREATE TABLE IF NOT EXISTS baskets(
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL,
        basketData JSONB NOT NULL,
        status TEXT NOT NULL
    );
    `

	_, err := r.Db.Exec(query)
	return err
}

func (r *PostgreSQLRepository) CreateBasket(basket model.Basket) (*model.Basket, error) {
	jsonData, err := json.Marshal(basket.BasketData)
	if err != nil {
		return nil, err
	}

	res, err := r.Db.Exec("INSERT INTO baskets(created_at, username, updated_at, basketData, status) VALUES($1, $2, $3, $4, $5)", basket.CreatedAt, basket.User, basket.UpdatedAt, jsonData, basket.Status)
	if err != nil {
		return nil, err
	}

	id, err := res.RowsAffected()
	if err != nil {
		return nil, err
	}
	basket.ID = id

	return &basket, nil
}

func (r *PostgreSQLRepository) AllBasket() ([]model.Basket, error) {
	rows, err := r.Db.Query("SELECT * FROM baskets")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var all []model.Basket
	for rows.Next() {
		var basket model.Basket
		var jsonData []byte
		if err := rows.Scan(&basket.ID, &basket.User, &basket.CreatedAt, &basket.UpdatedAt, &jsonData, &basket.Status); err != nil {
			return nil, err
		}
		basket.BasketData = string(jsonData)
		all = append(all, basket)
	}
	return all, nil
}

func (r *PostgreSQLRepository) GetByIdBasket(id int64) (*model.Basket, error) {
	row := r.Db.QueryRow("SELECT * FROM baskets WHERE id = $1", id)

	var basket model.Basket
	var jsonData []byte
	if err := row.Scan(&basket.ID, &basket.User, &basket.CreatedAt, &basket.UpdatedAt, &jsonData, &basket.Status); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNotExists
		}
		return nil, err
	}
	basket.BasketData = string(jsonData)
	return &basket, nil
}

func (r *PostgreSQLRepository) GetByNameBasket(name string) ([]model.Basket, error) {
	rows, err := r.Db.Query("SELECT * FROM baskets WHERE username = $1", name)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var all []model.Basket
	for rows.Next() {
		var basket model.Basket
		var jsonData []byte
		if err := rows.Scan(&basket.ID, &basket.User, &basket.CreatedAt, &basket.UpdatedAt, &jsonData, &basket.Status); err != nil {
			return nil, err
		}
		basket.BasketData = string(jsonData)
		all = append(all, basket)
	}

	return all, nil
}

func (r *PostgreSQLRepository) UpdateBasket(id int64, updated model.Basket) (*model.Basket, error) {
	if id == 0 {
		return nil, errors.New("invalid updated ID")
	}

	jsonData, err := json.Marshal(updated.BasketData)
	if err != nil {
		return nil, err
	}

	res, err := r.Db.Exec("UPDATE baskets SET username = $1, created_at = $2, updated_at = $3, basketData = $4, status = $5 WHERE id = $6", updated.User, updated.CreatedAt, updated.UpdatedAt, jsonData, updated.Status, id)
	if err != nil {
		return nil, err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return nil, err
	}

	if rowsAffected == 0 {
		return nil, ErrUpdateFailed
	}

	return &updated, nil
}

func (r *PostgreSQLRepository) DeleteBasket(id int64) error {
	res, err := r.Db.Exec("DELETE FROM baskets WHERE id = $1", id)
	if err != nil {
		return err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return err
	}

	if rowsAffected == 0 {
		return ErrDeleteFailed
	}

	return nil
}

func (r *PostgreSQLRepository) InitUser() error {
	query := `
    CREATE TABLE IF NOT EXISTS users(
		id SERIAL PRIMARY KEY,
		username TEXT NOT NULL,
		password TEXT NOT NULL
	);
    `

	_, err := r.Db.Exec(query)
	return err
}

func (r *PostgreSQLRepository) CreateUser(user model.User) (*model.User, error) {
	res, err := r.Db.Exec("INSERT INTO users(username, password) VALUES($1, $2)", user.Username, user.Password)
	if err != nil {
		return nil, err
	}

	id, err := res.LastInsertId()
	if err != nil {
		return nil, err
	}
	user.ID = id

	return &user, nil
}

func (r *PostgreSQLRepository) CheckUserName(name string) error {
	row := r.Db.QueryRow("SELECT * FROM users WHERE username = $1", name)

	var user model.User
	if err := row.Scan(&user.ID, &user.Username, &user.Password); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return ErrNotExists
		}
		return err
	}
	return nil
}

func (r *PostgreSQLRepository) GetUser(name string) (*model.User, error) {
	row := r.Db.QueryRow("SELECT * FROM users WHERE username = $1", name)

	var user model.User
	if err := row.Scan(&user.ID, &user.Username, &user.Password); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNotExists
		}
		return nil, err
	}
	return &user, nil
}

func (r *PostgreSQLRepository) UpdateUser(id int64, updated model.User) (*model.User, error) {
	if id == 0 {
		return nil, errors.New("invalid updated ID")
	}
	res, err := r.Db.Exec("UPDATE users SET username = $1, password = $2 WHERE id = $3", updated.Username, updated.Password, id)
	if err != nil {
		return nil, err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return nil, err
	}

	if rowsAffected == 0 {
		return nil, ErrUpdateFailed
	}

	return &updated, nil
}

func (r *PostgreSQLRepository) DeleteUserByName(name string) error {
	res, err := r.Db.Exec("DELETE FROM users WHERE username = $1", name)
	if err != nil {
		return err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return err
	}

	if rowsAffected == 0 {
		return ErrDeleteFailed
	}

	return nil
}
